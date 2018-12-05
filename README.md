# Logs Analysis

A reporting tool for a fictional news website that prints reports to the terminal using SQL queries to analyze the log data with Python and a PostgreSQL database. The database contains newspaper articles, as well as the web server log for the site.

The `news` database includes three tables:

- The authors table includes information about the authors of articles.
- The articles table includes the articles themselves.
- The log table includes one entry for each time a user has accessed the site.

The report answers the following questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


## Requirements

- [Vagrant](https://www.vagrantup.com/downloads.html)
- [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)


## How to Run the Application

Once you have set up your environment, `cd` into the `vagrant` directory and fork this repository. In that directory, [download the data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called `newsdata.sql`. Put this file into the project directory inside the vagrant directory, which is shared with your virtual machine.

Load the site's data into your local database with the command `psql -d news -f newsdata.sql`.

Here's what this command does:

- psql — the PostgreSQL command line program
- -d news — connect to the database named news which has been set up for you
- -f newsdata.sql — run the SQL statements in the file newsdata.sql

Explore the tables using the `\dt` and `\d` table commands and select statements. Get a sense for what sort of information is in each column of these tables.

`\dt` — display tables — lists the tables that are available in the database.
`\d table` — (replace table with the name of a table) — shows the database schema for that particular table.


## Views

There is one view for the `get_error_days()` method. You will have to manually add this view to the news database for the report to run. The create view command used is:

```sql
CREATE VIEW errortable AS
SELECT time::date, count(*) AS error
FROM log
WHERE status = '404 NOT FOUND'
GROUP BY time::date
ORDER BY time::date;
```

## Reports

To run the reports, use the command `python newsdatadb.py` from the project directory. Results will be displayed in terminal. These are the methods used to generate the reports:

- `get_popular_articles()` Returns the most popular three articles of all time and their corresponding views.

- `get_popular_articles()` Returns the most popular authors of all time with their corresponding total article views.

- `get_error_days()` Returns all days where over 1% of link requests were errors.

For a sample of output, please view `output_example.txt`.


## Contributing

Pull requests will not be accepted, as this project was created for the FSND Udacity program.

For details, check out [CONTRIBUTING.md](CONTRIBUTING.md).

