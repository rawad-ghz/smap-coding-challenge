# User Consumption Dashboard Application

View the <a href="dashboard_demo.md" target="_blank">application usage</a> demo.

## Notes

### Environment

The application was developed and tested on a debian linux machine, using python 3.6 as suggested, however commands described in this document should probably run flawlessly on OSX or Windows too.

### Demonstration

For the purpose of demonstrating different ways of implementing features, the application code illustrates different coding styles and methods such as using:

- using django-rest-framework (DRF) as well as simple JSON Response views to return JSON data.
- using Class Based Views (CBVs) as well as function views as a method of implementing Views.
- management command flags and optional arguments

whereas consistency is key in corporate and collaborative software development.

# Application Initialization/ Reset

Having installed and activated a python 3.6 virtual environment the application can be initialized using:

```sh
(env) $ python -m pip install -r requirements.txt
(env) $ cd dashboard
(env) $ rm db.sqlite3
(env) $ python manage.py migrate
```

The application can be ran using:

```sh
(env) $ python manage.py runserver 127.0.0.1:8000
```
and would be accessed from <a href="http://127.0.0.1:8000" target="_blank">here</a>

# Models

In its simplest form (yet normalized) and in order for the requirements to be met, the applicaiton requires mainly two models `User` and `UserConsumption` where obviously the former stores User data and the latter User Consumption data.

# Import Data Command

An import data command was implemented in order to populate the application database from CSV files as required, it is intended to be used as follows:

```sh
(env) $ # python manage.py import file_name.csv
(env) $ python manage.py import data/user_data.csv
(env) $ python manage.py import data/user_data.csv
```

This command assumes a directory named `consumption` existing alongside the CSV file where it searches for user consumption data, thus assuring UserConsumption data is properly linked to EXISTING users and thus data integrity is assured.

The command uses django-orm's bulk insert in order to populate UserConsumption data for the purpose of being more performant yet it could be further optimized to use raw SQL or other Methods for additional performance optimization.
 
One or more of `DELIMITER`, `DATETIME_FORMAT`, `CONSUMPTION_INTERVAL` can be overridden as well such as:

```sh
(env) $ python manage.py import data/user_data.csv --delimiter=',' --format='%Y-%m-%d %H:%M:%S' --interval='30'
(env) $ python manage.py import data/user_data.csv --d=',' --f='%Y-%m-%d %H:%M:%S' --i='30'
```

# Application Views (server-side)

Two categories of views where implemented in the application as per the requirements:

- **API views**: returning JSON data either 
    - via DRF and custom serializer classes or
    - via simple JsonResponse views
- **Page views**:  returning templated HTML responses which in turn make use of API view (from the client-side) in order to display data and charts which are implemented using
    - Class Based Views or
    - Simple Function Views

There are three main Page views which are:
- the Dashboard or Home view
- user details view
- area details view

making use of API views such as:
- consumption view
- data by month
- user data by month
- area data by month

## HTML templates

Server-side HTML templates make use of django-template inheritance and code blocks

## API queries

Django-orm queries to be called by API views had been refactored into a separate `queries.py` file for the purpose of keeping the `models.py` module as clean as possible.

# Datatables and Chart (client-side)

For the purpose of making the user experience more usefull and rich, client-side datatables and charts were added to the application making use of the following client side libraries:

- **JQuery DataTables**: jquery based datatables
- **Chart.js**: simple JS charting library 

as well as **bootstrap** and required **JQuery**.

## Implementation (Datatables and Charts)

Basic JavaScript code was written in order to
- populate client-side _datatables_ and _charts_ with data consumed from REST APIs
- bind datatable events to update charts accordingly (summary view)

# Testing

Basic application tests covering REST API, Views and Management Command tests can be ran using the following:

```sh
(env) $ python manage.py test
```

## Notes (on testing)

`setUpClass` _class method_ is used instead of `setUp` _instance method_ to populate _Test fixtures_ **once** per class instead of being called before each test method.

Similarly `tearDownClass` had been used to clean up _Test fixtures_.

# Code Linting

Basic PEP8 code linting via `flake8`, can be ran using the following:

```sh
(env) $ python -m flake8 .
```

# Enhancements

The current implementation of this demo application could be further enhanced, some enhancements include:

- **Code**
    - enhance APIs and Import Data _management command_ to handle unexpected input...
- **UX/UI**
    - better use of bootstrap components/ themes enabling more responsive and mobile friendly UI
    - theme-ing datatables in order to provide a consistent bootstrap-based layout or using a bootstrap-based Datatables library instead
    - using different kinds of charts such as (scatter, candlestick...) better demonstrating business KPIs
- **Technology**
    - using component based/reactive UI libraries such as React or Vue.js.. maximizing code re-usability and boosting performance (through virtual DOM)
    - using JS/CSS bundlers such as webpack bundling code into _versioned, minified, single JS/CSS files_
- **Tests**
    - using coverage.py to insure maximum test coverage
    - using complexity tests to check code maintainablity

## Datetime in SQLite

A custom function class `YearMonth` had been introduced to be used by django-orm queries in `queries.py` in order to filter `UserConsumption` start field by **Month of Year**. Similar classes can be implemented to be able to filter by `DatetimeField`s.

Another way to implement it would be using `strptime` instead of `substring` see <a href="year_month.md" target="_blank">this</a> for more info :).

This limitation would be overcome when using RDBMS such as **Postgres**, where django-orm supports `Datatime` fields filtering out-of-the-box.

# Production Notes

In addition to the enhancement mentioned above, the application is certainly not suitable for deployment on production environments. Some of the reasons are it's lack of implementation/usage of:

- **User Authentication**: user login and authentication mechanisms
- **User Authorization**: user groups and permissions specifying user access rights to application pages and API
- **Tests**: thorough applicaiton and API tests
- **Browser Support**: testing the application on multiple browsers to ensure UI consistency
- **Logging**: disabling debug=True and enabling logging
- **Database**: a relational database management system for better performance and scalability

regarding code.

As well as

- **Automated Builds and Continuous Integration**: using automated build/test scripts and staging/production environments
- **Containerization**: making use of docker or other containerization technologies for easy deployment on staging/production environments
- **HTTPS**: making use of TLS/SSL for a secure connction to the application and application's API

regarding testing and deployment.

# Bonus

View the <a href="commands.md" target="_blank">commands</a> demo.
