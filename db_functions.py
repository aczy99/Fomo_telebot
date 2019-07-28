import sqlalchemy as db
import datetime
import pandas as pd


# Connecting to MySQL server at localhost using PyMySQL DBAPI
db_url = "mysql+pymysql://root:1234567a@localhost/app0"
engine = db.create_engine(db_url)
connection = engine.connect()

# Accessing the correct table
posts = db.Table("post", db.MetaData(), autoload=True, autoload_with=engine)
category = db.Table("category", db.MetaData(), autoload=True, autoload_with=engine)
posttocategory = db.Table(
    "posttocategory", db.MetaData(), autoload=True, autoload_with=engine
)
venue = db.Table("venue", db.MetaData(), autoload=True, autoload_with=engine)


# Fetching all data
def execute_fetching_all(query):
    return connection.execute(query).fetchall()


# Fetching the first data
def execute_fetching_first(query):
    return connection.execute(query).first()


# Querying for all rows of data
def query_all():
    query = db.select([posts])
    return execute_fetching_all(query)


# Forming dataframe with results
def dataframing(results):
    df = pd.DataFrame(results)
    df.columns = results[0].keys()
    return df


# Querying by category RETURNS list of posts
def query_category(filter):
    query = db.select([category.columns.id]).where(category.columns.title == filter)
    filter_id = execute_fetching_first(query)
    if filter_id is not None:
        filter_id = filter_id[0]
        query = db.select([posttocategory.columns.post_id]).where(
            posttocategory.columns.category_id == filter_id
        )
        posts_id = execute_fetching_all(query)
        lst = []
        for i in posts_id:
            id = i[0]
            query = db.select([posts]).where(posts.columns.id == id)
            lst.append(execute_fetching_first(query))
        df = pd.DataFrame(lst)
        df.columns = select_columns_all(posts)
        return df
    else:
        return filter_id


# Querying by venue RETURNS list of posts
def query_venue(filter):
    query = db.select([venue.columns.id]).where(venue.columns.description == filter)
    venue_id = execute_fetching_first(query)
    if venue_id is not None:
        venue_id = venue_id[0]
        query = db.select([posts]).where(posts.columns.venue_id == venue_id)
        results = execute_fetching_all(query)
        if len(results) != 0:
            return dataframing(results)
        else:
            return None
    else:
        return venue_id


# Querying by date RETURNS list of posts
def query_date(date_range):
    date_today = datetime.datetime.today()
    if date_range == "TODAY":
        filter = date_today
    elif date_range == "THIS WEEK":
        filter = date_today + datetime.timedelta(days=8)
    else:
        filter = date_today + datetime.timedelta(days=30)

    query = db.select([posts]).where(
        db.and_(
            posts.columns.date >= date_today,
            posts.columns.date < filter,
        )
    )
    results = execute_fetching_all(query)
    if len(results) != 0:
        return dataframing(results)
    else:
        return None


# Counting the number of rows in posts RETURNS int
def select_count(table):
    query = db.select([table])
    return len(execute_fetching_all(query))


# Viewing all the fields in table RETURNS list of fields [(sports,)]
def select_columns_all(table):
    return table.columns.keys()


# Viewing all categories in categories RETURNS list of categories [cat,]
def select_categories():
    query = db.select([category.columns.title])
    cat = execute_fetching_all(query)
    lst = []
    for i in cat:
        lst.append(i[0])
    return lst


# Viewing all venues description in venue RETURNS list of venues [(usc,)]
def select_venue():
    query = db.select([venue.columns.description])
    return execute_fetching_all(query)


# Finding venue that corresponds to venue-id RETURNS string of venue description
def find_venue(venue_id):
    query = db.select([venue.columns.description]).where(venue.columns.id == venue_id)
    return execute_fetching_first(query)[0]


# Finding category that corresponds to category-id RETURNS string of category title
def find_category(category_id):
    query = db.select([category.columns.title]).where(category.columns.id == category_id)
    return execute_fetching_first(query)[0]


def find_category_id(post_id):
    query = db.select([posttocategory.columns.category_id]).where(
        posttocategory.columns.post_id == post_id
    )
    category_id = execute_fetching_first(query)[0]
    return category_id



