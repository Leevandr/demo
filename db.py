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
              select p.id,
                     b.title as brand,
                     c.title as category,
                     p.title,
                     p.price,
                     p.discount,
                     p.image,
                     p.description
              from products p
                       join brands b on b.id = p.brand_id
                       join categories c on c.id = p.category_id
              where p.title like %s
                 or p.description like %s
                 or c.title like %s
                 or b.title like %s \
              """
        search_param = f"%{search}%"
        params = [search_param, search_param, search_param, search_param]

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

    def edit_product(self, item_id, title, category_id, brand_id, description, price, discount, image):
        with self.cursor() as cur:
            cur.execute("update products set title = %s,"
                        " category_id = %s,"
                        " brand_id = %s,"
                        " description = %s,"
                        " price = %s,"
                        " discount = %s,"
                        " image = %s"
                        " where products.id = %s",
                        (title, category_id, brand_id, description, price, discount, image, item_id))
            cur.connection.commit()

    def delete_product(self, item_id):
        with self.cursor() as cur:
            cur.execute("delete from products where id = %s", (item_id,))
            cur.connection.commit()

    def get_all_orders(self):
        with self.cursor() as cur:
            cur.execute("select * from orders")
        return cur.fetchall()

    def get_all_users(self):
        with self.cursor() as cur:
            cur.execute("select * from users")
        return cur.fetchall()

    def get_all_statuses(self):
        with self.cursor() as cur:
            cur.execute("select * from statuses")
        return cur.fetchall()

    def add_order(self,user_id, status_id, count, product_id):
        with self.cursor() as cur:
            cur.execute("insert into orders(user_id, status_id, count, product_id) values (%s,%s,%s,%s)",(user_id, status_id, count, product_id))
            cur.connection.commit()

    def get_user_by_id(self, user_id):
        with self.cursor() as cur:
            cur.execute("select * from users where id = %s", (user_id,))
        return cur.fetchone()

    def get_status_by_id(self, status_id):
        with self.cursor() as cur:
            cur.execute("select * from statuses where id = %s", (status_id,))
        return cur.fetchone()

    def get_product_by_id(self, product_id):
        with self.cursor() as cur:
            cur.execute("select * from products where id = %s", (product_id,))
        return cur.fetchone()

    def edit_order(self, order_id, user_id, status_id, count, product_id):
        with self.cursor() as cur:
            cur.execute("update orders set user_id = %s, status_id = %s, count = %s, product_id = %s where id = %s", (user_id, status_id, count, product_id, order_id))
            cur.connection.commit()
            print("УСПЕХ, 1 200 000")

    def get_order_by_product(self, product_id):
        with self.cursor() as cur:
            cur.execute("select * from orders o where o.product_id = %s", (product_id, ))
        return cur.fetchall()

    def delete_order(self, order_id):
        with self.cursor() as cur:
            cur.execute("delete from orders where id = %s", (order_id, ))
            cur.connection.commit()
dao = Database()
