"""Storage abstractions for persisting created profiles."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List

from .models import AbstractProfile


class AbstractStorage(ABC):
    """Interface for storing created profiles."""

    @abstractmethod
    def add(self, profile: AbstractProfile) -> None:
        """Persist a profile instance."""

    @abstractmethod
    def all(self) -> Iterable[AbstractProfile]:
        """Return all stored profiles."""


class InMemoryStorage(AbstractStorage):
    """A simple in-memory storage used for demonstration and tests."""

    def __init__(self) -> None:
        self._items: List[AbstractProfile] = []

    def add(self, profile: AbstractProfile) -> None:
        self._items.append(profile)

    def all(self) -> Iterable[AbstractProfile]:
        return list(self._items)
