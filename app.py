import re
import sqlite3
import time

from flask import Flask, request
from flask import send_from_directory

from sender import Sender

# from flask_cors import CORS

app = Flask(__name__)
# CORS(app, origins="https://example.com")  # 添加 origins 参数以限制允许的来源

request_in_progress = False


def init_db():
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images
                 (id TEXT PRIMARY KEY , prompt TEXT, status TEXT)''')
    conn.commit()
    conn.close()


def clear_database(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM images")
    conn.commit()
    conn.close()


# 24小时刷新数据库
def clear_database_every_24_hours(db_path):
    while True:
        time.sleep(24 * 60 * 60)  # 等待24小时（24小时 * 60分钟 * 60秒）
        clear_database(db_path)


def extract_uuid(filename):
    uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    match = re.search(uuid_pattern, filename)
    if match:
        return match.group(0)
    else:
        return None


def print_stored_data():
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


def get_message_id_from_db(filename, db_path):
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


def reset_request_in_progress():
    global request_in_progress
    request_in_progress = False


@app.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory('images', filename)


@app.route('/v1/api/midjourney/send', methods=['POST'])
def send():
    status = 1
    msg = "Generate task successfully"
    data = request.get_json()
    print(f'获取参数={data}')
    sender = Sender()
    sender.send(data)
    resp = {
        "status": status,
        "msg": msg
    }
    return resp


if __name__ == "__main__":
    init_db()
    db_path = 'images.db'
    # clear_db_thread = threading.Thread(target=clear_database_every_24_hours, args=(db_path,))
    # clear_db_thread.daemon = True  # 设置为守护线程，这样在主程序结束时，线程也会结束
    # clear_db_thread.start()
    app.run(debug=True, host='0.0.0.0')
