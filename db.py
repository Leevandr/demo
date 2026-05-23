import pymysql
from pymysql.cursors import DictCursor


class Database:
    def __init__(self):
        self.connect = pymysql.connect(
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

    def get_all_items(self, category="Все", search="", sort="Без сортировки"):
        sql = """
            select b.title as brand, c.title as category, p.title, p.price, p.discount, p.image
            from products p
            join brands b on b.id = p.brand_id
            join categories c on c.id = p.category_id
            where p.title like %s
        """
        params = [f"%{search}%"]

        if category != "Все":
            sql += " and c.title = %s"
            params.append(category)

        if sort == "По возрастанию цены":
            sql += " order by p.price asc"

        if sort == "По убыванию цены":
            sql += " order by p.price desc"

        with self.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    def get_all_categories(self):
        with self.cursor() as cur:
            cur.execute("select title from categories")
            return cur.fetchall()

    def get_all_brands(self):
        with self.cursor() as cur:
            cur.execute("select title from brands")
            return cur.fetchall()

    def add_product(self, title, category_id, brand_id, description, price, discount, image):
        with self.cursor() as cur:
            cur.execute(
                "insert into products (title, category_id, brand_id, description, price, discount, image) "
                "values (%s,%s,%s,%s,%s,%s,%s)",
                (title, category_id, brand_id, description, price, discount, image)
            )
            cur.connection.commit()

    def get_category_id(self, category):
        with self.cursor() as cur:
            cur.execute("select id from categories where title = %s", (category,))
            return cur.fetchone()

    def get_brand_id(self, brand):
        with self.cursor() as cur:
            cur.execute("select id from brands where title = %s", (brand,))
            return cur.fetchone()


dao = Database()
