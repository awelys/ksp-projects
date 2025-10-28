"""Command line interface for creating users and employees."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

import click

from user_management.factories import EmployeeFactory, UserFactory
from user_management.logger import Logger
from user_management.services import UserService
from user_management.storage import InMemoryStorage

VALID_MODES = {"create_user", "create_employee"}


def _collect_modes(values: Iterable[str]) -> List[str]:
    modes: List[str] = []
    for value in values:
        if not value:
            continue
        for mode in value.split(","):
            cleaned = mode.strip()
            if cleaned:
                modes.append(cleaned)
    return modes


def _load_from_file(path: Path) -> Dict[str, str]:
    params: Dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            raise click.UsageError(
                f"Строка '{stripped}' в файле {path} должна иметь формат ключ=значение"
            )
        key, value = stripped.split("=", 1)
        params[key.strip()] = value.strip()
    return params


def _merge_parameters(file_params: Dict[str, str], cli_params: Dict[str, Any]) -> Dict[str, Any]:
    combined: Dict[str, Any] = {}
    combined.update(file_params)
    for key, value in cli_params.items():
        if value is None:
            continue
        if isinstance(value, (list, tuple)) and not value:
            continue
        combined[key] = value
    return combined


def _prepare_modes(params: Dict[str, Any]) -> List[str]:
    mode_values: Iterable[str] = []
    if "mode" in params and params["mode"]:
        raw_mode = params["mode"]
        if isinstance(raw_mode, (list, tuple)):
            mode_values = raw_mode
        else:
            mode_values = [str(raw_mode)]
    modes = _collect_modes(mode_values)
    if not modes:
        raise click.UsageError(
            "Необходимо указать режим работы с помощью аргумента --mode"
        )
    for mode in modes:
        if mode not in VALID_MODES:
            raise click.UsageError(
                f"Неизвестный режим '{mode}'. Доступные режимы: {', '.join(sorted(VALID_MODES))}"
            )
    return modes


@click.command()
@click.option(
    "--mode",
    "mode",
    multiple=True,
    help="Режим работы: create_user, create_employee. Можно указать несколько значений",
)
@click.option("--lastname", "lastname", help="Фамилия пользователя")
@click.option("--firstname", "firstname", help="Имя пользователя")
@click.option("--telephone", "telephone", help="Номер телефона")
@click.option("--address", "address", help="Адрес пользователя")
@click.option("--position", "position", help="Должность сотрудника")
@click.option(
    "--salary",
    "salary",
    type=float,
    help="Зарплата сотрудника. Используется для режима create_employee",
)
@click.option(
    "--file",
    "file_",
    type=click.Path(exists=True, path_type=Path),
    help="Путь к текстовому файлу с параметрами в формате ключ=значение",
)
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    help="Путь к файлу для сохранения результата в формате JSON",
)
def cli(
    mode: Iterable[str],
    lastname: str | None,
    firstname: str | None,
    telephone: str | None,
    address: str | None,
    position: str | None,
    salary: float | None,
    file_: Path | None,
    output: Path | None,
) -> None:
    """Создать пользователя или сотрудника на основе аргументов командной строки."""

    file_params: Dict[str, Any] = {}
    if file_ is not None:
        file_params = _load_from_file(file_)

    cli_params: Dict[str, Any] = {
        "mode": list(mode),
        "lastname": lastname,
        "firstname": firstname,
        "telephone": telephone,
        "address": address,
        "position": position,
        "salary": salary,
    }
    params = _merge_parameters(file_params, cli_params)

    modes = _prepare_modes(params)

    logger = Logger("user-cli")
    storage = InMemoryStorage()
    service = UserService(
        storage=storage,
        user_factory=UserFactory(logger=logger),
        employee_factory=EmployeeFactory(logger=logger),
    )

    created = []
    for current_mode in modes:
        if current_mode == "create_user":
            required_fields = ["lastname", "firstname", "telephone", "address"]
            missing = [field for field in required_fields if not params.get(field)]
            if missing:
                raise click.UsageError(
                    "Для создания пользователя необходимо указать: "
                    + ", ".join(missing)
                )
            created.append(
                service.create_user(
                    lastname=params["lastname"],
                    firstname=params["firstname"],
                    telephone=params["telephone"],
                    address=params["address"],
                ).to_dict()
            )
        elif current_mode == "create_employee":
            required_fields = [
                "lastname",
                "firstname",
                "telephone",
                "address",
                "position",
            ]
            missing = [field for field in required_fields if not params.get(field)]
            if missing:
                raise click.UsageError(
                    "Для создания сотрудника необходимо указать: "
                    + ", ".join(missing)
                )
            created.append(
                service.create_employee(
                    lastname=params["lastname"],
                    firstname=params["firstname"],
                    telephone=params["telephone"],
                    address=params["address"],
                    position=params["position"],
                    salary=params.get("salary", 0.0) or 0.0,
                ).to_dict()
            )

    result_json = json.dumps(created, ensure_ascii=False, indent=2)
    click.echo(result_json)

    if output is not None:
        output.write_text(result_json, encoding="utf-8")
        click.echo(f"Результат сохранен в файл {output}")


if __name__ == "__main__":
    cli()
