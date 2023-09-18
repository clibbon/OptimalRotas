"""Classes to manage schedules"""

from optimalrotas.exceptions import NoEmployeesLeftException
from .data_types import Employee, EmployeePool, Project
from .exceptions import AlreadyStaffedException
from datetime import date, timedelta
from typing import Union
from .util import DAYS_PER_WEEK


PROJECT_NAME_LEN_CHARS = 20
PROJECT_COL_TITLE = "Week Number"


class StaffedProject:
    """A project with staff assigned to it"""

    project: Project
    assigments: dict[str, Union[Employee, None]]

    def __init__(self, project: Project) -> None:
        self.project = project
        self.assigments = {role_id: None for role_id in project.team_needed.keys()}

    @classmethod
    def from_assignments(
        cls, project: Project, assignments: dict[str, Union[Employee, None]]
    ):
        """If assignments are already known, create a staffed project"""
        staffed = cls(project)
        staffed.assign_multiple(assignments)
        return staffed

    def check_role(self, role_id):
        """Checks a role exists in this project"""
        if role_id not in self.assigments:
            raise IndexError(f"{role_id} doesn't exist")

    def get_roles(self) -> list[str]:
        """Returns a list of roles in this project"""
        return list(self.assigments.keys())

    def assign(self, role_id: str, employee: Employee) -> None:
        """Adds an employee to a role, raises an error if the role is already full"""
        self.check_role(role_id)

        role_already_staffed = self.assigments[role_id] is not None
        if role_already_staffed:
            raise AlreadyStaffedException(f"Role {role_id} is already staffed")

        self.assigments[role_id] = employee

    def assign_or_replace(
        self, role_id: str, employee: Union[Employee, None]
    ) -> Union[Employee, None]:
        """Adds an employee to a role, replacing anyone already assigned"""
        self.check_role(role_id)

        previously_assigned = self.assigments[role_id]
        self.assigments[role_id] = employee
        return previously_assigned

    def assign_multiple(
        self, new_assignments: dict[str, Union[Employee, None]]
    ) -> None:
        """Assign multiple roles at once"""
        assert new_assignments.keys() == self.assigments.keys(), "Role IDs do not match"
        self.assigments.update(new_assignments)


def randomly_staff_project(project: Project, available_staff: EmployeePool):
    """Staff a project using a pool"""
    assigned_roles = {}

    for role_id, role in project.team_needed.items():
        try:
            employee = available_staff.get_by_role(role)
            assigned_roles[role_id] = employee
        except NoEmployeesLeftException:
            assigned_roles[role_id] = None

    return StaffedProject.from_assignments(project, assigned_roles)


class Schedule:
    assignments: list[StaffedProject]

    def __init__(self) -> None:
        self.assignments = []

    @classmethod
    def from_assignments(cls, assignments: list[StaffedProject]):
        schedule = Schedule()
        schedule.assignments.extend(assignments)

    @classmethod
    def from_projects(cls, projects: list[Project], pool: EmployeePool):
        schedule = Schedule()
        staffed_projects = []

        for project in projects:
            staffed_projects.append(randomly_staff_project(project, pool))

        schedule.assignments = staffed_projects
        return schedule

    def display(self) -> str:
        """Returns a formatted string showing the current schedule and assigned
        people"""
        first_monday = self.get_first_monday()
        last_monday = self.get_last_monday()
        n_weeks = (last_monday - first_monday).days // DAYS_PER_WEEK
        week_number_strings = "".join([f"{i + 1:>3}" for i in range(n_weeks)])
        output_strings = [
            " " * PROJECT_NAME_LEN_CHARS + "Week Number",
            (
                PROJECT_COL_TITLE
                + " " * (PROJECT_NAME_LEN_CHARS - len(PROJECT_COL_TITLE))
                + week_number_strings
            ),
        ]

        for staffed_project in sorted(
            self.assignments,
            key=lambda x: (
                get_previous_monday(x.project.start_date),
                get_previous_monday(x.project.end_date),
            ),
        ):
            output_string = self.make_display_row(
                first_monday, last_monday, n_weeks, staffed_project
            )
            row_title = get_project_name_for_display(
                staffed_project.project.project_name
            )
            output_strings.append(row_title + output_string)

        return "\n".join(output_strings)

    def make_display_row(self, first_monday, last_monday, n_weeks, staffed_project):
        """Makes a single row of the schedule display based on the project timeline.

        For example ___######__________ where the #'s indicate the project duration"""
        project_first_monday = get_previous_monday(staffed_project.project.start_date)
        project_last_monday = get_previous_monday(staffed_project.project.end_date)

        start_weeks = (project_first_monday - first_monday).days // DAYS_PER_WEEK
        end_weeks = (last_monday - project_last_monday).days // DAYS_PER_WEEK
        project_length = n_weeks - start_weeks - end_weeks

        output_string = "___" * start_weeks
        output_string += "###" * project_length
        output_string += "___" * end_weeks
        return output_string

    def get_first_monday(self) -> date:
        """Returns the first Monday across all the projects"""
        earliest_start_date = min(
            project.project.start_date for project in self.assignments
        )
        return get_previous_monday(earliest_start_date)

    def get_last_monday(self) -> date:
        """Returns the last Monday across all the projects"""
        latest_end_date = max(project.project.end_date for project in self.assignments)
        return get_previous_monday(latest_end_date)


def get_project_name_for_display(project_name) -> str:
    """Return a project name ready for display"""
    if len(project_name) >= PROJECT_NAME_LEN_CHARS:
        return project_name[: PROJECT_NAME_LEN_CHARS - 1] + ":"
    else:
        n_spaces_required = PROJECT_NAME_LEN_CHARS - len(project_name) - 1
        return project_name + " " * n_spaces_required + ":"


def get_previous_monday(input_date: date) -> date:
    """Get the previous Monday - if already a Monday return the current date"""
    return input_date - timedelta(days=input_date.weekday())
