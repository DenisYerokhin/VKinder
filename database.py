import psycopg2
from configuration import database, user, password

with psycopg2.connect(
              database=database,
              user=user,
              password=password
) as conn:
    conn.commit()

def viewed_people_create_table():
    with conn.cursor() as cur:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS viewed_people(
            id serial
            id_vk varchar(80) PRIMARY KEY);"""
        )

def viewed_people_save_information(conn, id_vk):
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO viewed_people(id_vk) VALUES(%s);""",
            (id_vk)
        )

def checking_user_data():
    with conn.cursor() as cur:
        cur.execute(
            """SELECT vp.vk_id FROM viewed_people AS vp;"""
        )
        return cur.fetchall()

def viewed_people_delete_table():
    with conn.cursor() as cur:
        cur.execute(
            """DROP TABLE viewed_people;"""
        )
