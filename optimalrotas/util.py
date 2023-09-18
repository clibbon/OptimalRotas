from datetime import date, timedelta
from random import randint, choices
from .data_types import Role, Project

DAYS_PER_WEEK = 7
ROLES = [role for role in Role]  # Annoying Enum thing


def create_random_project(
    min_start_date: date,
    max_end_date: date,
    min_project_length_weeks: int = 3,
    max_project_length_weeks: int = 20,
    min_staff: int = 3,
    max_staff: int = 12,
):
    """Generates a random project with random staffing requirements between
    the two listed dates"""
    if (max_end_date - min_start_date).days // DAYS_PER_WEEK < max_project_length_weeks:
        raise ValueError(
            f"Max date {max_end_date} must be at least {max_project_length_weeks} weeks after"
            " {min_start_date}"
        )

    max_start_date = max_end_date - timedelta(days=max_project_length_weeks * DAYS_PER_WEEK)
    n_possible_days = (max_start_date - min_start_date).days
    random_start_date = min_start_date + timedelta(days=randint(0, n_possible_days))
    random_project_length_days = (
        randint(min_project_length_weeks, max_project_length_weeks) * DAYS_PER_WEEK
    )
    end_date = random_start_date + timedelta(days=random_project_length_days)

    random_n_staff = randint(min_staff, max_staff)
    staff = choices(ROLES, k=random_n_staff)

    return Project(random_start_date, end_date, staff)
