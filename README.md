## Problem Background

```
You've been hired onto a team working on a newspaper site. The user-facing newspaper site frontend itself, and the database behind it, are already built and running. You've been asked to build an **internal reporting tool** that will use information from the database to discover what kind of articles the site's readers like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity.

The program you write in this project will run from the command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the answers to some questions.
```

### Data Location

[Download the data from here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

### Loading the data

1. Create the database ***news*** 

    ` DROP DATABASE news;`   

    `CREATE DATABASE news;`  


2. Import the data using the below command  

 `psql -U username -d news -f newsdata.sql`

***username*** - It's the username with which you want to connect  

***-d*** - It corresponds to the database name  

***-f*** - It's the **full file path**  



### Some Questions which we are trying to answer

1. **What are the most popular three articles of all time?** Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

> Example:
> * "Princess Shellfish Marries Prince Handsome" — 1201 views
> * "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
> * "Political Scandal Ends In Political Scandal" — 553 views

2. **Who are the most popular article authors of all time?** That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

> Example:
> * Ursula La Multa — 2304 views
> * Rudolf von Treppenwitz — 1985 views
> * Markoff Chaney — 1723 views
> * Anonymous Contributor — 1023 views


3. **On which days did more than 1% of requests lead to errors?** The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)

> Example:
> * July 29, 2016 — 2.5% errors

### Usage

``` > python newsdata.py ```  


### DB Username and password  


I have stored my postgres db username and password in **environment variables** so that the username and 
password will not be exposed

To run it either you can store the password and username in **environment variables** and use it or else

*hardcode*[Not recommended] them in the *** newsdb.py *** file line no: 6,7

