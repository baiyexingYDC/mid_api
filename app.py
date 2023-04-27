import re

from flask import Flask, request

from db import Db
from sender import Sender

# from flask_cors import CORS

app = Flask(__name__)
# CORS(app, origins="https://example.com")  # 添加 origins 参数以限制允许的来源


def extract_uuid(filename):
    uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    match = re.search(uuid_pattern, filename)
    if match:
        return match.group(0)
    else:
        return None



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
    db = Db()
    db.init()
    app.run(debug=True, host='0.0.0.0')
