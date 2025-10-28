"""Service layer combining factories and storage."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .factories import EmployeeFactory, UserFactory
from .models import AbstractProfile, Employee, User
from .storage import AbstractStorage


@dataclass
class UserService:
    """High level API used by the CLI to manage users."""

    storage: AbstractStorage
    user_factory: UserFactory
    employee_factory: EmployeeFactory

    def create_user(self, **data: str) -> User:
        user = self.user_factory.create(**data)
        self.storage.add(user)
        return user

    def create_employee(self, **data: str) -> Employee:
        employee = self.employee_factory.create(**data)
        self.storage.add(employee)
        return employee

    def all_profiles(self) -> Iterable[AbstractProfile]:
        return self.storage.all()
