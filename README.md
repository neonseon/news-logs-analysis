# Logs Analysis

A reporting tool that prints reports to the terminal using Python and PostgreSQL.


## How to Run the Application

Run the command `python newsdatadb.py` to run the reports. Results will be displayed in terminal. These are the methods used to generate the reports:

- `get_popular_articles()` Returns the most popular three articles of all time and their corresponding views.

- `get_popular_articles()` Returns the most popular authors of all time with their corresponding total article views.

- `get_error_days()` Returns all days where over 1% of link requests were errors.

For a sample of output, please view `output_example.txt`.


## Views

There is one view for the `get_error_days()` method. The create view command used is:

```create view errortable as
select time::date, count(*) as error
from log where status = '404 NOT FOUND'
group by time::date order by time::date;
```

## Contributing

Pull requests will not be accepted, as this project was created for the FSND Udacity program.

For details, check out [CONTRIBUTING.md](CONTRIBUTING.md).

