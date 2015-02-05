"""Tests for the views of the freckle_budgets app."""
from django.test import RequestFactory, TestCase

from mock import patch

from . import fixtures
from .. import views


class YearViewTestCase(TestCase):
    """Tests for the ``YearView`` view."""
    longMessage = True

    def test_view(self):
        with patch('freckle_budgets.freckle_api.get_entries') as entries_mock:  # NOQA
            entries_mock.return_value = fixtures.get_api_response(self)
            req = RequestFactory().get('/')
            resp = views.YearView.as_view()(req, year=self.year.year)
            self.assertEqual(resp.status_code, 200, msg=('View is callable'))
