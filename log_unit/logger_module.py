from enum import Enum
import threading
import datetime
from typing import TYPE_CHECKING

# Define the Enum
Severity = Enum('Severity', [('DEBUG', 10), ('INFO', 20), ('WARNING', 30), ('ERROR', 40), ('CRITICAL', 50)])


class _ActionLogger:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self.logs = []

    def log(self, message: str, severity: Severity = Severity.INFO, add_timestamp: bool = True) -> None:
        """Logs a message to the logger.

        Args:
            message: The message to be logged.
            severity: The severity of the message to be logged: DEBUG, INFO, WARNING, ERROR, CRITICAL.
            add_timestamp: Whether to add the timestamp to the logs.
        """

        lvl_str = severity.name
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with self._lock:
            if add_timestamp:
                self.logs.append(f"[{timestamp}] [{lvl_str}] [{message}]")
            else:
                self.logs.append(f"[{lvl_str}] [{message}]")

    def clear(self) -> None:
        """Clears all stored logs."""
        with self._lock:
            self.logs = []

    def __str__(self) -> str:
        """Returns all logs as a single newline-separated string."""
        with self._lock:
            return "\n".join(self.logs)

    def save_to_file(self, filename: str = "logfile.log") -> None:
        """Saves current logs to a file.

        Args:
            :param filename: The path of the file to save the logs to."""
        with self._lock:
            with open(filename, "a") as f:
                f.write(str(self) + "\n")


logger = _ActionLogger()
