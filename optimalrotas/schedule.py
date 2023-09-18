"""Classes to manage schedules"""

from data_types import Employee, Project
from datetime import date


class StaffedProject:
    """A project with staff assigned to it"""

    project: Project
    assigments: dict[str, Employee]

    def __init__(self) -> None:
        pass


class Schedule:
    assignments: list[StaffedProject]

    def display(self) -> None:
        """Returns a formatted string showing the current schedule and assigned
        people"""
        first_monday = self.get_first_monday()
        last_monday = self.get_last_monday()

    def get_first_monday(self) -> date:
        """Returns the first Monday across all the projects"""
        pass

    def get_last_monday(self) -> date:
        """Returns the last Monday across all the projects"""
        pass
