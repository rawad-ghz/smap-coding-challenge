# Year Month Implementation

The **optimal way** to get the month of the year in SQLite would be

```sql
SELECT strftime('%Y%m', start) AS "year_month" from consumption_userconsumption limit 1;
-- results in 201903 (for example)
```

which might be implemented in django-orm creating a custom class inheriting from `Func` base class such as:

```python
class YearMonth(Func):
    function = 'strftime'
    template = "%(function)s('%Y%m', %(expressions)s)"  # could not escape % character
    output_field = models.CharField()
```

however this wont work due to the inablity to escape `%` characters in string templates.

Thus an alternative **without percentage (%)** implementation was introduced and `substr` was chosen to solve this issue:

```python
class YearMonth(Func):
    """UserConsumption start column filter to filter by month of year %Y-%m"""
    template = "substr(%(expression)s, 0, 8)"
    output_field = models.CharField()
```

resulting in a query along the lines of:

```sql
SELECT substr(start, 0, 8) AS "year_month" from consumption_userconsumption limit 1;
-- results in 2019-03 (for example)
```

where results can be grouped by `year_month` in order to aggregate data by month.
