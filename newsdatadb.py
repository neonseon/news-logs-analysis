#!/usr/bin/env python2
#
# "Database code" for the Logs Analysis Project.

import psycopg2

DBNAME = "news"


def get_popular_articles():
    """Return the most popular three articles of all time."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
      SELECT initcap(articles.title), num
      FROM (SELECT path, count(*) AS num
      FROM log
      GROUP BY path
      ORDER BY num DESC) log JOIN articles
      ON log.path = '/article/' || articles.slug
      LIMIT 3;
    """)
    articles = c.fetchall()
    db.close()
    print "\nMost popular articles of all time:"
    for title, views in articles:
        print('* "{}" - {} views'.format(title, views))


def get_popular_authors():
    """Return the most popular authors of all time."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
      SELECT authors.name, sum(num) AS views
      FROM (SELECT path, count(*) AS num
      FROM log
      GROUP BY path
      ORDER BY num DESC) log JOIN articles
      ON (log.path LIKE '%' || articles.slug) JOIN authors
      ON authors.id = articles.author
      GROUP BY authors.name
      ORDER BY views DESC;
    """)
    authors = c.fetchall()
    db.close()
    print "\nMost popular authors of all time:"
    for name, views in authors:
        print('* {} - {} views'.format(name, views))


def get_error_days():
    """Return days where over 1% of requests were errors."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
      SELECT to_char(time::date, 'FMMonth FMDD, YYYY')
      AS date, round(percentage, 2) AS errors
      FROM (SELECT log.time::date,(error::decimal/(success + error) * 100.0)
      AS percentage
      FROM (SELECT time::date, count(*) AS success
      FROM log
      WHERE status = '200 OK'
      GROUP BY time::date
      ORDER BY time::date) log JOIN errortable
      ON log.time::date = errortable.time::date
      GROUP BY log.time::date, errortable.error, log.success
      ORDER BY log.time::date) AS total
      WHERE percentage > 1
    """)
    days = c.fetchall()
    db.close()
    print "\nDays where over 1% of requests were errors:"
    for date, errors in days:
        print('* {} - {} % errors'.format(date, errors))


if __name__ == '__main__':
    get_popular_articles()
    get_popular_authors()
    get_error_days()
