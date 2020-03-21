import psycopg2
from os import environ

DBNAME = 'news'
CONN_DICT = {}
CONN_DICT['user'] = environ.get('PSQL_SU')
CONN_DICT['password'] = environ.get('PSQL_SU_PASS')
CONN_DICT['database'] = DBNAME

def get_tables(conn_dict=CONN_DICT):

    try:
        conn = psycopg2.connect(**conn_dict) # dictionary unpacking
        cursor = conn.cursor()

        # To fetch the table details
        cursor.execute("SELECT table_name FROM information_schema.tables \
        WHERE table_schema = 'public'")

        tables = cursor.fetchall()
        # The above returns a tuple like ('tablename',)

        # for table in tables:
        #     print("> ", table)

        conn.close()
        return tables

    except Exception as e:
        print("Error: ",e)

def get_column_names(tables, conn_dict=CONN_DICT):
    try:
        conn = psycopg2.connect(**conn_dict)
        cursor = conn.cursor()

        for table in tables:
            print("table > ", table[0])
            cursor.execute("SELECT column_name FROM information_schema.columns \
                where table_name = %s",table)
            columns = cursor.fetchall()
            print(columns)

        conn.close()
    except Exception as e:
        print("Error: ", e)


def most_popular_articles(howmany=3, conn_dict=CONN_DICT):
    """
    This method returns the most popular articles from the news database

    Strategy:
        1. from log table fetch the path and extract article name
        2. group by the article name
        3. count the no of rows
        4. return a tuple of article-name and his count
    """
    query = """ SELECT X.article_name,
       count(X.article_name) AS article_cnt
FROM
  (SELECT PATH,
          status,
          position('/article/' IN PATH) AS article_position,
          substring(PATH
                    FROM position('/article/' IN PATH)+length('/article/')) AS article_name
   FROM log) X
WHERE X.article_position > 0
GROUP BY X.article_name
ORDER BY article_cnt DESC
LIMIT %s """

    try:
        conn = psycopg2.connect(**conn_dict)
        cursor = conn.cursor()
        cursor.execute(query, (howmany,))
        articles_list = cursor.fetchall()
        # for article_tuple in articles_list:
        #     print(article_tuple)

        conn.close()
        return articles_list
    except Exception as e:
        print("Error: ", e)



def most_popular_authors(conn_dict=CONN_DICT):
    """
    This method returns the most popular article authors from the news database

    Strategy:
        1. from log table fetch the path and extract article
        2. join the article and author
        3. group by author name
        4. count the no of rows
        5. return a tuple of author-name and his count
    """
    query = """
    select   Au.name as author_name, sum(Y.article_cnt) as author_reviews

from
(select X.article_name as a_name, count(X.article_name) as article_cnt
from 
	(select path, status, position('/article/' in path) as article_position, 
	substring(path from  position('/article/' in path)+length('/article/')) as article_name
	from log) X 
where X.article_position > 0 group by X.article_name order by article_cnt desc) Y , 

	authors Au, articles Ar where Ar.slug = Y.a_name and Ar.author = Au.id 
	group by Au.name order by author_reviews desc

    """
    
    try:
        conn = psycopg2.connect(**conn_dict)
        cursor = conn.cursor()
        cursor.execute(query)
        authors_list = cursor.fetchall()
        # for author_tuple in authors_list:
        #     print(author_tuple)
        conn.close()
        return authors_list
    except Exception as e:
        print("Error: ", e)

def request_errors(threshold=(0.01,),conn_dict=CONN_DICT ):
    """
    This method returns the most popular article authors from the news database

    Strategy:
        1. group the log table based on the status code 
        2. write another query which queries the above result set with added
        column of ratio which is (bad/total-reqs)
        3. return a tuple of date and its ratio which is above the threshold
    """
    query = """
    select X.dt, TRUNC((Y.f_req *1.0/X.t_req)*100 ,2) as thresh
        from 
        (select date(time) as dt, count(date(time)) as t_req 
        from 
        log 
        group by date(time)
        ) X,
        (select date(time) as dt, count(status) as f_req 
        from log 
        where status = '404 NOT FOUND' 
        group by date(time), status
        ) Y
        where X.dt = Y.dt and (Y.f_req *1.0/X.t_req) > %s 
        order by thresh desc
    """
    try:
        conn = psycopg2.connect(**conn_dict)
        cursor = conn.cursor()
        cursor.execute(query, threshold)
        failed_reqs = cursor.fetchall()
        # for failed_req in failed_reqs:
        #     print(failed_req)
        conn.close()
        return failed_reqs
    except Exception as e:
        print("Error: ", e)



# most_popular_articles()
# most_popular_authors()
# request_errors()


        


