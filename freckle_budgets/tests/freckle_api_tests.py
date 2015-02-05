"""Tests for the Freckle api client of the freckle_budgets app."""
from django.test import TestCase

from . import fixtures
from .. import freckle_api
from .. import models


class GetProjectTimesTestCase(TestCase):
    """Tests for the ``get_project_times`` function."""
    longMessage = True

    def test_function(self):
        entries = fixtures.get_api_response(self)
        projects = models.Project.objects.get_for_year(self.year.year)

        expected = {
            1: {
                111: {
                    1111: 5,
                    'total': 5,
                    'project_name': 'Project 111',
                },
                222: {
                    2222: 8,
                    'total': 8,
                    'project_name': 'Project 222',
                },
            },
            2: {
                222: {
                    2222: 16,
                    'total': 16,
                    'project_name': 'Project 222',
                },
                333: {
                    1111: 32,
                    'total': 32,
                    'project_name': 'Project 333',
                },
            },
        }

        result = freckle_api.get_project_times(projects, entries)
        self.assertEqual(list(result), list(expected), msg=(
            'Should turn the list of entries into a dict that has months as'
            ' keys and each month is a dict that has project IDs as keys and'
            ' the final values is the total minutes booked on that project'
            ' in that month.'))
