import psycopg2
from psycopg2 import sql


db_params = {
    'dbname': 'botbase',
    'user': 'annaerm',
    'password': 'qwer1234',
    'host': 'localhost',
    'port': '5432',
}

create_table_query = """
CREATE TABLE IF NOT EXISTS public.groups
(
    id integer NOT NULL DEFAULT nextval('groups_id_seq'::regclass),
    name text,
    CONSTRAINT groups_pkey PRIMARY KEY (id)
)
"""

create_table_address = """"
CREATE TABLE IF NOT EXISTS address (
    id SERIAL PRIMARY KEY,
    name TEXT,
    color TEXT
)
"""

with psycopg2.connect(**db_params) as conn:
    with conn.cursor() as cur:
        cur.execute(create_table_query)
        cur.execute(create_table_address)
        conn.commit()


conn.close()
