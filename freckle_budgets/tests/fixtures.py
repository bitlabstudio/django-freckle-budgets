"""Test-fixtures for the freckle_budgets app."""
from mixer.backend.django import mixer


def create_month(cls):
    """Creates one ``Month`` object."""
    cls.month = mixer.blend(
        'freckle_budgets.Month', month=1, year__year=2015,
        year__sick_leave_days=12, year__vacation_days=12, year__rate=100,
        public_holidays=1, employees=2)


def create_project_months(cls):
    """Creates two ``ProjectMonth`` objects."""
    create_month(cls)
    cls.proj1 = mixer.blend(
        'freckle_budgets.Project', is_investment=False, freckle_project_id='1')
    cls.proj2 = mixer.blend(
        'freckle_budgets.Project', is_investment=True, freckle_project_id='2')
    cls.project_month1 = mixer.blend(
        'freckle_budgets.ProjectMonth', project=cls.proj1,
        month=cls.month, budget=1000, rate=100, )
    cls.project_month2 = mixer.blend(
        'freckle_budgets.ProjectMonth', project=cls.proj2,
        month=cls.month, budget=2000, rate=200, )


def get_api_response():
    """
    Returns a typical freckle API response and creates necessary objects.

    """
    year = mixer.blend('freckle_budgets.Year', year=2015)
    mixer.blend(
        'freckle_budgets.ProjectMonth', project__freckle_project_id='proj1',
        month__year=year)
    mixer.blend(
        'freckle_budgets.ProjectMonth', project__freckle_project_id='proj2',
        month__year=year)
    mixer.blend(
        'freckle_budgets.ProjectMonth', project__freckle_project_id='proj3',
        project__is_investment=True, month__year=year)

    entries = [
        {
            # First project, first month, billable hours
            'entry': {
                'date': '2015-01-01',
                'project_id': 'proj1',
                'billable': True,
                'minutes': 1,
            }
        },
        {
            # Unbillable hours should not be added up
            'entry': {
                'date': '2015-01-01',
                'project_id': 'proj1',
                'billable': False,
                'minutes': 2,
            }
        },
        {
            # Billable hours should be added up
            'entry': {
                'date': '2015-01-02',
                'project_id': 'proj1',
                'billable': True,
                'minutes': 4,
            }
        },
        {
            # Another project in the same month
            'entry': {
                'date': '2015-01-02',
                'project_id': 'proj2',
                'billable': True,
                'minutes': 8,
            }
        },
        {
            # Another month
            'entry': {
                'date': '2015-02-01',
                'project_id': 'proj2',
                'billable': True,
                'minutes': 16,
            }
        },
        {
            # Unbillable hours for investment projects should be added up
            'entry': {
                'date': '2015-02-01',
                'project_id': 'proj3',
                'billable': False,
                'minutes': 32,
            }
        },
    ]
    return entries
