"""Factory classes that encapsulate profile creation logic."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from .logger import Logger
from .models import AbstractProfile, Employee, User


class AbstractProfileFactory(ABC):
    """Base factory for profile creation."""

    def __init__(self, logger: Logger | None = None) -> None:
        self.logger = logger or Logger(self.__class__.__name__)

    @abstractmethod
    def create(self, **data: Any) -> AbstractProfile:
        """Create a profile using the provided *data*."""


class UserFactory(AbstractProfileFactory):
    """Factory producing :class:`~user_management.models.User` objects."""

    def create(self, **data: Any) -> User:
        return User(
            lastname=data["lastname"],
            firstname=data["firstname"],
            telephone=data["telephone"],
            address=data["address"],
            logger=self.logger,
        )


class EmployeeFactory(UserFactory):
    """Factory creating :class:`~user_management.models.Employee` instances."""

    def create(self, **data: Any) -> Employee:
        return Employee(
            lastname=data["lastname"],
            firstname=data["firstname"],
            telephone=data["telephone"],
            address=data["address"],
            position=data["position"],
            salary=float(data.get("salary", 0.0)),
            logger=self.logger,
        )
