"""Templatetags for the freckle_budgets app."""
import calendar

from django import template

from .. import utils


register = template.Library()


@register.assignment_tag
def get_hours_left(project_month, entries_times):
    """Returns the hours left in order to fulfill the budget time."""
    budget_hours = project_month.get_budget_hours()
    try:
        time_tracked = entries_times[project_month.month.month][
            int(project_month.project.freckle_project_id)]
    except KeyError:
        return budget_hours
    return (budget_hours * 60.0 - time_tracked) / 60.0


@register.assignment_tag
def get_weeks(month):
    """Returns the days for a month as a list of weeks."""
    return calendar.Calendar(0).monthdatescalendar(
        month.year.year, month.month)


@register.assignment_tag
def get_workloads(month):
    """Calls the same method on the Month model."""
    return month.get_workloads()


@register.assignment_tag
def get_workload(workloads, workload):
    """
    Returns the item from the dict with the given key.

    Somehow this doesn't seem to work via normal templating language in this
    case.

    """
    return workloads[workload]


@register.assignment_tag
def is_available_workday(day, month):
    """
    ``True`` if the given day is available as a workday in the given month.

    Example: January has 22 workdays. If you deduct public holidays, you end up
    with 21 available work days.

    We want to render the last X days of the month differently to show that
    these days are not really available because the staff was absent due to the
    holidays.

    """
    work_days = month.get_work_days(
        minus_sick_leave=False, minus_vacations=False)
    workday = utils.get_workday_number(day)
    return workday <= work_days


@register.assignment_tag
def is_budget_fulfilled(entries_times, project, day):
    try:
        total_time = entries_times[project.month.month][
            int(project.project.freckle_project_id)]
    except KeyError:
        return False
    daily_hours = project.get_daily_hours()
    days_fulfilled = total_time / (daily_hours * 60)
    workday = utils.get_workday_number(day)
    if workday <= days_fulfilled:
        return True
    return False
