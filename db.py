import pymysql
from pymysql.cursors import DictCursor


class Database:
    def __init__(self):
        self.connect = pymysql.connect (
            host="localhost",
            port=3308,
            database="sport_plus",
            user="root",
            password="",
            cursorclass=DictCursor
        )


    def cursor(self):
        return self.connect.cursor()

    def login(self, login, passw):
        with self.cursor() as cur:
            cur.execute("select * from users where username = %s and password = %s", (login, passw))
            return cur.fetchone()

    def get_all_items(self):
        with self.cursor() as cur:
            cur.execute("select b.title as brand, c.title as category, p.title, p.price, p.discount, p.image "
                        "from products p "
                        "join brands b using(id) "
                        "join categories c using(id)")
            return cur.fetchall()

dao=Database()