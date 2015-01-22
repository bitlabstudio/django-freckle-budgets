Django Freckle Budgets
======================

A reusable Django app that allows to plan year budgets and track them via letsfreckle.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-freckle-budgets

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/django-freckle-budgets.git#egg=freckle_budgets

TODO: Describe further installation steps (edit / remove the examples below):

Add ``freckle_budgets`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'freckle_budgets',
    )

Add the ``freckle_budgets`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^freckle-budgets/', include('freckle_budgets.urls')),
    )

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate freckle_budgets

Finally make sure to add the necessary settings to your ``local_settings.py``:


.. code-block:: python
    FRECKLE_BUDGETS_ACCOUNT_NAME = 'your-freckle-account-name' 
    FRECKLE_BUDGETS_API_TOKEN = 'your-freckle-api-token' 


Usage
-----

Add a year
++++++++++

The first thing you need to do is to add a year via the Django admin:

* **Year**: This is the year you want to add, i.e. 2015
* **Rate**: This is your hourly rate that you would like to get for new
  projects in this year. This value will be used to calculate the potential
  amount of money you could earn if you were fully booked out (one can be
  allowed to dream).
* **Work hours per day**: The number of hours you will definitely work on each
  work day.
* **Sick leave days**: The number of sick leave days that you estimate (this is
  per person, not the total for all employees) 
* **Vacation days**: The number of vacation days that each employee may take
  during this year.

These values will be used to calculate the total number of hours that your team
can possibly work during any month.

Add months
++++++++++

Once you have added a year, you need to add twelve months for that year via the
Django admin:

* **Year**: The year this month belongs to.
* **Month**: The month number (i.e. 1 for January)
* **Number of employees**: The number of employees that you will have during
  this month.
* **Public holidays**: The number of public holidays that this month has in
  this year.

Again, these values are mainly needed to calculate the total number of hours
that your team can work during this month.

Add projects
++++++++++++

After adding a year and it's months, you need to add a few projects via the
Django admin:

* **Name**: The display name for this project.
* **Freckle project ID**: The project ID of this project in your freckle
  account.
* **Color**: A CSS color code for this project (i.e. ``#C7B06F``)
* **Is investment**: If you are working on this project for free (i.e. for
  internal projects), enable this checkbox.

Add project budgets to months
+++++++++++++++++++++++++++++

For each of your projects, add as many ``ProjectMonth`` objects as needed. For
example, if you have a long running project that has budgets for the whole
year, you would have to add twelve objects:

* **Project**: The project you want to plan for.
* **Month**: The month you want to plan for.
* **Budget**: The budget that you can burn on this project during this month.
* **Rate**: The hourly rate that you can bill for this project.

Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-freckle-budgets
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch

In order to run the tests, simply execute ``tox``. It will create two more
venvs and run tests against Django 1.6 and Django 1.7.
