from pathlib import Path

from flask import Flask, render_template
from werkzeug.middleware.dispatcher import DispatcherMiddleware

import BMI
import diemhocphan
import maytinh

# Thư mục chứa file HTML: D:\bt chuong 5\html
HTML_DIR = Path(__file__).resolve().parent.parent / "html"

app = Flask(__name__, template_folder=str(HTML_DIR))

ITEMS = [
    {"icon": "🧮", "title": "Máy tính cơ bản",    "desc": "Cộng, trừ, nhân, chia.",              "url": "/maytinh/"},
    {"icon": "🎓", "title": "Tính điểm học phần", "desc": "Từ điểm CC, GK, CK ra điểm chữ.",     "url": "/diemhocphan/"},
    {"icon": "⚖️", "title": "Tính chỉ số BMI",    "desc": "Từ chiều cao, cân nặng ra BMI.",       "url": "/bmi/"},
]


@app.route("/")
def index():
    return render_template("menu.html", items=ITEMS)


# Gắn 3 app con vào các đường dẫn tương ứng
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/maytinh": maytinh.app.wsgi_app,
    "/diemhocphan": diemhocphan.app.wsgi_app,
    "/bmi": BMI.app.wsgi_app,
})

if __name__ == "__main__":
    app.run(debug=True)