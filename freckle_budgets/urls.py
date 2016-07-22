"""URLs for the freckle_budgets app."""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<year>\d+)$', views.YearView.as_view(), name='freckle_budgets_year_view'),
]
