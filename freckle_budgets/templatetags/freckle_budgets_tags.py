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
