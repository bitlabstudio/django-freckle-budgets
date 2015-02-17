"""
Helper method to fetch data from the Freckle API.

See http://developer.letsfreckle.com

"""
import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from freckle_client.client import FreckleClientV2


client = FreckleClientV2(access_token=settings.FRECKLE_BUDGETS_ACCESS_TOKEN)


def get_entries(projects, start_date, end_date):  # pragma: no cover
    """
    Returns the entries for the given project and time frame.

    :param start_date: String representing the start date (YYYY-MM-DD).
    :param end_date: String representing the end date (YYYY-MM-DD).

    """
    entries = client.fetch_json(
        'entries',
        query_params={
            'per_page': 1000,
            'search[from]': start_date,
            'search[to]': end_date,
            'search[projects]': ','.join(
                [project.freckle_project_id for project in projects]),
        }
    )
    return entries


def get_project_times(projects, entries):
    """
    Returns a dict with total time tracked per project / employee.

    The dict should look like this:

        {
            month: {
                project_id: {
                    user_id-1: XX,
                    user_id-2: YY,
                    total: XX + YY,
                },
            },
        }

    """
    result = {}
    for entry in entries:
        entry_date = datetime.datetime.strptime(
            entry['date'], '%Y-%m-%d')
        if entry_date.month not in result:
            result[entry_date.month] = {}
        project_id = entry['project']['id']
        project_name = entry['project']['name']
        user_id = entry['user']['id']
        try:
            project = projects.get(freckle_project_id=project_id)
        except ObjectDoesNotExist:
            project = None
        if project_id not in result[entry_date.month]:
            result[entry_date.month][project_id] = {
                'total': 0, 'project_name': project_name, }
            if project is None:
                result[entry_date.month][project_id]['is_planned'] = False
            else:
                result[entry_date.month][project_id]['is_planned'] = True
        if user_id not in result[entry_date.month][project_id]:
            result[entry_date.month][project_id][user_id] = 0
        if (project and project.is_investment) or entry['billable']:
            minutes = entry['minutes']
            result[entry_date.month][project_id][user_id] += minutes
            result[entry_date.month][project_id]['total'] += minutes
    return result
