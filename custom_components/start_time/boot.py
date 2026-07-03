"""Boot time capture for the Start Time integration.

Home Assistant does not expose its boot duration through a public API: the
value only exists as the argument of the ``"Home Assistant initialized in
%.2fs"`` log record emitted by ``homeassistant.bootstrap`` at the end of
startup. :class:`BootTimeMonitor` is a standard :class:`logging.Filter`
attached to that logger to read the value without altering logging behavior
(the record always passes through). It is detached on config entry unload.
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

    def filter(self, record: logging.LogRecord) -> bool:
        """Inspect the record for the boot message; always let it through."""
        if (
            self.boot_time is None
            and isinstance(record.msg, str)
            and record.msg.startswith(BOOT_MESSAGE_PREFIX)
            and isinstance(record.args, tuple)
            and record.args
            and isinstance(record.args[0], (int, float))
        ):
            self._set_boot_time(float(record.args[0]))
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
            self._listeners.remove(listener)

        self._listeners.append(listener)
        return _remove

    def attach(self) -> None:
        """Start monitoring the bootstrap logger."""
        logging.getLogger(BOOTSTRAP_LOGGER_NAME).addFilter(self)

    def detach(self) -> None:
        """Stop monitoring the bootstrap logger and drop listeners."""
        logging.getLogger(BOOTSTRAP_LOGGER_NAME).removeFilter(self)
        self._listeners.clear()
