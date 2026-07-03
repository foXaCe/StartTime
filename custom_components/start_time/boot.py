"""Boot time capture for the Start Time integration.

Home Assistant does not expose its boot duration through a public API: the
value only exists as the argument of the ``"Home Assistant initialized in
%.2fs"`` log record emitted by ``homeassistant.bootstrap`` at the end of
startup. :class:`BootTimeMonitor` is a standard :class:`logging.Filter`
attached to that logger to read the value without altering logging behavior
(records the user would normally see always pass through). It is detached on
config entry unload.

The boot message is logged at INFO and Python only consults logger filters
after the level check: with e.g. ``logger: default: warning`` the record
would never be created and the capture would never fire. ``attach()``
therefore lowers the bootstrap logger to INFO when needed, while ``filter()``
re-enforces the original threshold so the user-visible logs are unchanged;
``detach()`` restores the original level.
"""

from __future__ import annotations

import logging
from collections.abc import Callable

from .const import BOOT_MESSAGE_PREFIX, BOOTSTRAP_LOGGER_NAME

_LOGGER = logging.getLogger(__name__)

type BootTimeListener = Callable[[float], None]


class BootTimeMonitor(logging.Filter):
    """Capture the Home Assistant boot duration from the bootstrap log record."""

    def __init__(self) -> None:
        """Initialize the monitor with no captured value."""
        super().__init__()
        self.boot_time: float | None = None
        self._listeners: list[BootTimeListener] = []
        self._original_level: int = logging.NOTSET
        self._suppress_below: int | None = None

    def filter(self, record: logging.LogRecord) -> bool:
        """Inspect the record for the boot message; keep visible logs as-is."""
        if (
            self.boot_time is None
            and isinstance(record.msg, str)
            and record.msg.startswith(BOOT_MESSAGE_PREFIX)
            and isinstance(record.args, tuple)
            and record.args
            and isinstance(record.args[0], (int, float))
        ):
            self._set_boot_time(float(record.args[0]))
        if self._suppress_below is not None:
            # attach() lowered the logger level to make this filter run:
            # drop the records the original configuration would have dropped.
            return record.levelno >= self._suppress_below
        return True

    def _set_boot_time(self, value: float) -> None:
        """Store the captured boot duration and notify listeners."""
        self.boot_time = round(value, 2)
        _LOGGER.debug("Captured boot time: %.2f s", self.boot_time)
        for listener in list(self._listeners):
            listener(self.boot_time)

    def add_listener(self, listener: BootTimeListener) -> Callable[[], None]:
        """Register a listener called on capture; return an unsubscribe callable."""

        def _remove() -> None:
            # Tolerant: detach() may already have cleared the listeners.
            if listener in self._listeners:
                self._listeners.remove(listener)

        self._listeners.append(listener)
        return _remove

    def attach(self) -> None:
        """Start monitoring the bootstrap logger.

        If the effective level is above INFO (e.g. ``logger: default:
        warning``), the boot record would be dropped before filters run.
        Lower the logger to INFO and let :meth:`filter` re-enforce the
        original threshold so nothing extra reaches the handlers.
        """
        logger = logging.getLogger(BOOTSTRAP_LOGGER_NAME)
        effective = logger.getEffectiveLevel()
        if effective > logging.INFO:
            self._original_level = logger.level
            self._suppress_below = effective
            logger.setLevel(logging.INFO)
        logger.addFilter(self)

    def detach(self) -> None:
        """Stop monitoring the bootstrap logger and drop listeners."""
        logger = logging.getLogger(BOOTSTRAP_LOGGER_NAME)
        logger.removeFilter(self)
        if self._suppress_below is not None:
            logger.setLevel(self._original_level)
            self._original_level = logging.NOTSET
            self._suppress_below = None
        self._listeners.clear()
