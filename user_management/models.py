"""Domain models for the user management module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict
from uuid import UUID, uuid4

from .logger import Logger


@dataclass
class AbstractProfile(ABC):
    """Common fields for every profile in the system."""

    lastname: str
    firstname: str
    telephone: str
    address: str
    id: UUID = field(default_factory=uuid4, init=False)
    logger: Logger = field(default_factory=Logger, repr=False)

    entity_name: str = "profile"

    def __post_init__(self) -> None:
        self.logger.log(
            f"Creating {self.entity_name}: {self.firstname} {self.lastname}"
        )
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        """Perform extra validation in subclasses."""

    def to_dict(self) -> Dict[str, str]:
        """Represent the profile as a JSON-serialisable dictionary."""

        return {
            "id": str(self.id),
            "lastname": self.lastname,
            "firstname": self.firstname,
            "telephone": self.telephone,
            "address": self.address,
            "type": self.entity_name,
        }


@dataclass
class User(AbstractProfile):
    """Basic system user."""

    entity_name: str = "user"

    def validate(self) -> None:  # pragma: no cover - trivial validation for example
        if not self.lastname or not self.firstname:
            raise ValueError("A user must have both firstname and lastname")


@dataclass
class Employee(User):
    """Company employee profile."""

    position: str = ""
    salary: float = 0.0
    entity_name: str = "employee"

    def __post_init__(self) -> None:
        super().__post_init__()
        self.logger.log(
            f"Assigning position '{self.position}' with salary {self.salary:.2f}"
        )

    def validate(self) -> None:
        super().validate()
        if not self.position:
            raise ValueError("Employee position cannot be empty")
        if self.salary < 0:
            raise ValueError("Employee salary cannot be negative")

    def to_dict(self) -> Dict[str, str]:
        data = super().to_dict()
        data.update({
            "position": self.position,
            "salary": self.salary,
        })
        return data
