"""Unit tests for the BootTimeMonitor logging filter."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from custom_components.start_time.boot import BootTimeMonitor
from custom_components.start_time.const import BOOTSTRAP_LOGGER_NAME

if TYPE_CHECKING:
    import pytest


def _record(msg: object, args: tuple[object, ...]) -> logging.LogRecord:
    """Build a log record as emitted by homeassistant.bootstrap."""
    return logging.LogRecord(
        BOOTSTRAP_LOGGER_NAME, logging.INFO, __file__, 0, msg, args, None
    )


def test_captures_boot_time_and_lets_record_through() -> None:
    """The boot message is captured, rounded, and the record passes."""
    monitor = BootTimeMonitor()
    assert monitor.filter(_record("Home Assistant initialized in %.2fs", (25.184,)))
    assert monitor.boot_time == 25.18


def test_ignores_unrelated_messages() -> None:
    """Other bootstrap records leave the monitor untouched."""
    monitor = BootTimeMonitor()
    assert monitor.filter(_record("Setting up stage 2", ()))
    assert monitor.filter(_record("Starting Home Assistant", ()))
    assert monitor.boot_time is None


def test_ignores_message_without_numeric_arg() -> None:
    """A boot-like message without a usable argument is ignored."""
    monitor = BootTimeMonitor()
    assert monitor.filter(_record("Home Assistant initialized in %.2fs", ()))
    assert monitor.filter(_record("Home Assistant initialized in %s", ("fast",)))
    assert monitor.filter(_record(42, (1.0,)))
    assert monitor.boot_time is None


def test_first_capture_wins() -> None:
    """Only the first boot message of the process is kept."""
    monitor = BootTimeMonitor()
    monitor.filter(_record("Home Assistant initialized in %.2fs", (10.0,)))
    monitor.filter(_record("Home Assistant initialized in %.2fs", (99.0,)))
    assert monitor.boot_time == 10.0


def test_listener_notified_and_unsubscribed() -> None:
    """Listeners get the captured value; unsubscribing stops notifications."""
    monitor = BootTimeMonitor()
    received: list[float] = []
    unsubscribe = monitor.add_listener(received.append)

    monitor.filter(_record("Home Assistant initialized in %.2fs", (12.345,)))
    assert received == [12.35]

    unsubscribe()
    assert not monitor._listeners  # noqa: SLF001


def test_attach_and_detach_manage_logger_filters() -> None:
    """attach() registers on the bootstrap logger; detach() cleans up fully."""
    logger = logging.getLogger(BOOTSTRAP_LOGGER_NAME)
    monitor = BootTimeMonitor()
    monitor.add_listener(lambda _: None)

    monitor.attach()
    try:
        assert monitor in logger.filters
    finally:
        monitor.detach()

    assert monitor not in logger.filters
    assert not monitor._listeners  # noqa: SLF001


def test_unsubscribe_after_detach_is_safe() -> None:
    """Unsubscribing after detach() cleared the listeners must not raise."""
    monitor = BootTimeMonitor()
    unsubscribe = monitor.add_listener(lambda _: None)
    monitor.attach()
    monitor.detach()
    unsubscribe()  # listeners already cleared — must be tolerant
    assert not monitor._listeners  # noqa: SLF001


def test_end_to_end_through_real_logging() -> None:
    """A real log call on the bootstrap logger is captured transparently."""
    logger = logging.getLogger(BOOTSTRAP_LOGGER_NAME)
    monitor = BootTimeMonitor()
    monitor.attach()
    try:
        logger.info("Home Assistant initialized in %.2fs", 42.128)
    finally:
        monitor.detach()
    assert monitor.boot_time == 42.13


def test_captures_despite_warning_default_level() -> None:
    """`logger: default: warning` must not break the capture.

    The boot record is emitted at INFO and Python checks the logger level
    before consulting filters: without the attach() level handling the
    record would never be created and the sensor would stay unknown forever.
    """
    logger = logging.getLogger(BOOTSTRAP_LOGGER_NAME)
    previous = logger.level
    logger.setLevel(logging.WARNING)
    monitor = BootTimeMonitor()
    try:
        monitor.attach()
        logger.info("Home Assistant initialized in %.2fs", 33.333)
        assert monitor.boot_time == 33.33
        monitor.detach()
        assert logger.level == logging.WARNING  # original level restored
    finally:
        monitor.detach()  # idempotent
        logger.setLevel(previous)


def test_visible_logs_unchanged_while_level_lowered(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Lowering the level must not surface records the user had silenced."""
    logger = logging.getLogger(BOOTSTRAP_LOGGER_NAME)
    previous = logger.level
    logger.setLevel(logging.WARNING)
    monitor = BootTimeMonitor()
    try:
        monitor.attach()
        with caplog.at_level(logging.DEBUG):
            logger.info("Home Assistant initialized in %.2fs", 12.345)
            logger.info("Setting up stage 1")
            logger.warning("Something worth seeing")
        assert monitor.boot_time == 12.35
        # INFO records stay invisible, exactly as the user configured...
        assert "initialized" not in caplog.text
        assert "Setting up stage 1" not in caplog.text
        # ...while WARNING and above still get through.
        assert "Something worth seeing" in caplog.text
    finally:
        monitor.detach()
        logger.setLevel(previous)


def test_inherited_level_restored_to_notset() -> None:
    """When the threshold comes from the root logger, NOTSET is restored."""
    root = logging.getLogger()
    logger = logging.getLogger(BOOTSTRAP_LOGGER_NAME)
    previous_root, previous = root.level, logger.level
    logger.setLevel(logging.NOTSET)
    root.setLevel(logging.WARNING)
    monitor = BootTimeMonitor()
    try:
        monitor.attach()
        assert logger.level == logging.INFO
        monitor.detach()
        assert logger.level == logging.NOTSET
    finally:
        monitor.detach()
        root.setLevel(previous_root)
        logger.setLevel(previous)
