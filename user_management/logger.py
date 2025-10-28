"""Simple logger utilities for the user management module."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from typing import TextIO


@dataclass
class Logger:
    """A lightweight logger used for demonstrating aggregation."""

    name: str = "user-management"
    stream: TextIO = sys.stdout

    def log(self, message: str) -> None:
        """Log *message* prepended with a timestamp and logger name."""

        timestamp = datetime.now().isoformat(sep=" ", timespec="seconds")
        print(f"[{timestamp}] {self.name}: {message}", file=self.stream)
