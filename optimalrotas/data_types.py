"""Data types used in the rotas project

Thanks to:
https://fivethirtyeight.datasettes.com/fivethirtyeight/most-common-name~2Fsurnames for the list of names used 
in the random employee generator.
https://www.mit.edu/~ecprice/wordlist.10000 for the list of random words used to generate project names
"""

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from enum import Enum
from random import choice, choices, sample
from typing import Optional

from .exceptions import NoEmployeesLeftException
from .resources import RESOURCES_PATH

RANDOM_NAMES_FILENAME = "popular_names.txt"
RANDOM_WORDS = None
RANDOM_WORDS_FILENAME = "ecprice_wordlist.1000.txt"


class Role(Enum):
    """Types of roles that can be requested in projects"""

    COMMERCIAL = 1
    TECHNICAL = 2
    OVERSIGHT = 3


@dataclass
class Employee:
    """Represents an individual to be added to the rota"""

    name: str
    role: Role


class EmployeePool:
    """A pool of employees helping create schedules"""

    def __init__(self, employees: list[Employee]) -> None:
        self.pool = defaultdict(list)

        for employee in employees:
            self.pool[employee.role].append(employee)

    def __repr__(self) -> str:
        n_employees = sum(len(v) for v in self.pool.values())
        return f"EmployeePool with {len(self.pool.keys())} roles and {n_employees} employees"

    @classmethod
    def random_names(cls, n_employees: int = 10):
        """Create a new employee pool with"""

        with open(RESOURCES_PATH / RANDOM_NAMES_FILENAME, "r", encoding="utf-8") as f:
            names = f.readlines()
        roles = list(Role)

        assert n_employees <= len(
            names
        ), f"Choose less than {len(names)} employees as I only have this many names"

        random_employess = [
            Employee(name, choice(roles)) for name in sample(names, n_employees)
        ]
        return EmployeePool(random_employess)

    def get_by_role(self, role: Role) -> Employee:
        """Attempt to get an employee of the defined role type."""
        try:
            return self.pool[role].pop()
        except IndexError as exc:
            raise NoEmployeesLeftException(
                f"No employees of type {role.name} available"
            ) from exc

    def add(self, employee: Employee):
        """Adds an employee to the pool"""
        self.pool[employee.role].append(employee)

    def update(self, employees: list[Employee]):
        """Adds a list of employees to the pool"""
        for employee in employees:
            self.add(employee)


@dataclass
class Project:
    """Defines the requirements of a project"""

    team_needed: dict[str, Role]
    start_date: date
    end_date: date
    project_name: str

    def __init__(self, start_date: date, end_date: date, team: list[Role], project_name: Optional[str] = None) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.team_needed = {}
        self.project_name = project_name if project_name is not None else create_random_name()

        counter = Counter()
        for role in team:
            counter.update([role])
            self.team_needed[f"{role.name}_{counter[role]}"] = role


def get_random_words():
    """Lazy load random words list"""

    global RANDOM_WORDS

    if RANDOM_WORDS is None:
        with open(RESOURCES_PATH / RANDOM_WORDS_FILENAME, "r", encoding="utf-8") as f:
            RANDOM_WORDS = [line.strip() for line in f.readlines()]

    return RANDOM_WORDS


def create_random_name(n_words=2):
    """Generates a random name as a series of random words joined by underscores"""
    return "_".join(choices(get_random_words(), k=n_words))
