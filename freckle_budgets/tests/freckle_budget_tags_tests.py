"""Tests for the templatetags of the freckle_budgets app."""
import calendar
import datetime

from django.test import TestCase

from mock import MagicMock, patch

from mixer.backend.django import mixer

from . import fixtures
from .. import models
from .. import freckle_api
from ..templatetags import freckle_budgets_tags as tags


class GetHoursLeftTestCase(TestCase):
    """Tests for the ``get_hours_left`` templatetag."""
    longMessage = True

    def test_tag(self):
        with patch('freckle_budgets.freckle_api.requests.request') as request_mock:  # NOQA
            request_mock.return_value = MagicMock()
            request_mock.return_value.status_code = 200
            request_mock.return_value.json = MagicMock()
            request_mock.return_value.json.return_value = \
                fixtures.get_api_response(self)

            projects = models.Project.objects.get_for_year(self.year.year)
            client = freckle_api.FreckleClient('foobar', 'token')
            entries = client.get_entries(projects, '2015-0101', '2015-12-31')
            entries_times = freckle_api.get_project_times(projects, entries)

            # this should be month2, proj2
            result = tags.get_hours_left(
                self.proj2_month2, entries_times)
            self.assertEqual(round(result, 2), 9.73, msg=(
                'Should substract the tracked hours from the total budget'
                ' hours'))

            result = tags.get_hours_left(
                self.proj3_month1, entries_times)
            self.assertEqual(round(result, 2), 10.00, msg=(
                'Should not crash if for the given projects no freckle'
                ' timings are present'))


class GetWeeksTestCase(TestCase):
    """Tests for the ``get_weeks`` assignment tag."""
    longMessage = True

    def test_tag(self):
        month = mixer.blend('freckle_budgets.Month', year__year=2015, month=1)
        expected = calendar.Calendar(0).monthdatescalendar(2015, 1)
        result = tags.get_weeks(month)
        self.assertEqual(result, expected, msg=(
            'Should return a list of weeks. Each list is a list of days'))


class IsAvailableWorkdayTestCase(TestCase):
    """Tests for the ``is_available_workday`` assignment tag."""
    longMessage = True

    def test_tag(self):
        year = mixer.blend('freckle_budgets.Year', year=2015,
            sick_leave_days=12, vacation_days=24)
        month = mixer.blend('freckle_budgets.Month', year=year,
            month=1, public_holidays=1)
        day = datetime.date(2015, 1, 1)
        result = tags.is_available_workday(day, month)
        self.assertTrue(result, msg=(
            'The first day of the month should obviously be shown as an'
            ' available workday'))

        day = datetime.date(2015, 1, 26)
        result = tags.is_available_workday(day, month)
        self.assertTrue(result, msg=(
            'January has 22 work days. Minus 2 vacation days and one'
            ' sick-leave day and one public holiday, we are left with 18'
            ' available work days. Therefore, the 26th (which is the 18th'
            ' workday) should be available.'))

        day = datetime.date(2015, 1, 27)
        result = tags.is_available_workday(day, month)
        self.assertFalse(result, msg=(
            'Based on the calculation above, the 27th should be the first'
            ' workday that is no longer available'))


class IsBudgetFulfilledTestCase(TestCase):
    """Tests for the ``is_budget_fulfilled`` assignment tag."""
    longMessage = True

    def test_tag(self):
        project_month = mixer.blend(
            'freckle_budgets.ProjectMonth', budget=1000, rate=100)
        entries_times = {
            1: {101: 5, 102: 8, },
            2: {102: 16}
        }
        day = datetime.date(2015, 01, 01)

        result = tags.is_budget_fulfilled(entries_times, project_month, day)
        self.assertFalse(result, msg=(
            'Should return false when the project ID cannot be found in the'
            ' entries_times dict'))

        project_month = mixer.blend(
            'freckle_budgets.ProjectMonth',
            budget=1000, rate=100, project__freckle_project_id=101,
            month__public_holidays=0, month__year__year=2015, month__month=1,
            month__year__work_hours_per_day=5, month__year__sick_leave_days=0,
            month__year__vacation_days=0)

        result = tags.is_budget_fulfilled(entries_times, project_month, day)
        self.assertFalse(result, msg=(
            'This project needs 0.45hrs per day but we have only fulfilled'
            ' 5 minutes so far, so no day has been fulfilled, yet'))

        day = datetime.date(2015, 1, 5)
        entries_times[1][101] = 82
        result = tags.is_budget_fulfilled(entries_times, project_month, day)
        self.assertTrue(result, msg=(
            'This project needs 0.45hrs per day (27.27 minutes) and we have'
            ' fulfilled 82 minutes so far, so three days have been fulfilled,'
            ' already'))

        day = datetime.date(2015, 1, 6)
        result = tags.is_budget_fulfilled(entries_times, project_month, day)
        self.assertFalse(result, msg=(
            'Sanity check for the test above. If three days are fulfilled,'
            ' the fourth workday should not be fulfilled'))
