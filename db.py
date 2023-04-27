import sqlite3
import yaml

class Db:

    def __init__(self):
        with open('config.yaml') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.db_path = config['db_path']

    def init(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS mj_prompt_task
                     (id INTEGER PRIMARY KEY , prompt TEXT, status TEXT)''')
        conn.commit()
        conn.close()

    def add_mj_prompt_task(self, prompt):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("insert into mj_prompt_task (prompt, status) values (?, '0')", (prompt,))
        conn.commit()
        conn.close()

    def print_stored_data(self):
        conn = sqlite3.connect('images.db')
        c = conn.cursor()
        c.execute("SELECT * FROM images")
        rows = c.fetchall()
        conn.close()

        print("Stored data in the database:")
        print("message_id | url | filename")
        print("---------------------------------------------")
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]}")

    def get_message_id_from_db(self, filename, db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 查询数据库以获取与 filename 相关联的 message_id
        cursor.execute("SELECT message_id FROM images WHERE filename=?", (filename,))
        result = cursor.fetchone()

        if result:
            message_id = result[0]
        else:
            message_id = None

        conn.close()
        return message_id

    def clear_database(self, db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("DELETE FROM images")
        conn.commit()
        conn.close()