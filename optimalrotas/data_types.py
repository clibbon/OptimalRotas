"""Data types used in the rotas project"""

from dataclasses import dataclass
from enum import Enum
from datetime import date
from collections import Counter


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


@dataclass
class Project:
    """Defines the requirements of a project"""
    team_needed: dict[str, Role]
    start_date: date
    end_date: date

    def __init__(self, start_date: date, end_date: date,
                 team: list[Role]) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.team_needed = {}

        counter = Counter()
        for role in team:
            counter.update([role])
            self.team_needed[f"{role.name}_{counter[role]}"] = role
