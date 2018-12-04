#!/usr/bin/env python2
#
# "Database code" for the Logs Analysis Project.

import psycopg2

DBNAME = "news"


def get_popular_articles():
    """Return the most popular three articles of all time."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select initcap(articles.title), num from (select path," +
              " count(*) as num from log group by path order by num desc)" +
              " log join articles on" +
              " (log.path like '%' || articles.slug) limit 3")
    articles = c.fetchall()
    db.close()
    print "\nMost popular articles of all time:"
    for x in articles:
        print('* "' + x[0] + '" - ' + str(x[1]) + ' views')


def get_popular_authors():
    """Return the most popular authors of all time."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select authors.name, sum(num) as views from" +
              " (select path, count(*) as num from log group by path" +
              " order by num desc) log" +
              " join articles on (log.path like '%' || articles.slug)" +
              " join authors on authors.id = articles.author" +
              " group by authors.name order by views desc")
    authors = c.fetchall()
    db.close()
    print "\nMost popular authors of all time:"
    for x in authors:
        print("* " + x[0] + " - " + str(x[1]) + " views")


def get_error_days():
    """Return days where over 1% of requests were errors."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select to_char(time::date, 'FMMonth FMDD, YYYY') as date," +
              " round(percentage, 2) as errors from (select log.time::date," +
              " (error::decimal/success * 100.0) as percentage" +
              " from (select time::date, count(*) as success from log" +
              " where status = '200 OK' group by time::date" +
              " order by time::date) log join errortable" +
              " on log.time::date = errortable.time::date" +
              " group by log.time::date, errortable.error, log.success" +
              " order by log.time::date) as total where percentage > 1")
    days = c.fetchall()
    db.close()
    print "\nDays where over 1% of requests were errors:"
    for x in days:
        print("* " + x[0] + " - " + str(x[1]) + "% errors\n")


get_popular_articles()
get_popular_authors()
get_error_days()
