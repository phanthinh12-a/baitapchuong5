import re
from pathlib import Path

from flask import Flask, render_template, request

# Thư mục chứa file HTML: D:\bt chuong 5\html
HTML_DIR = Path(__file__).resolve().parent.parent / "html"

app = Flask(__name__, template_folder=str(HTML_DIR))

NUMBER_RE = re.compile(r"^[+-]?(\d+([.,]\d*)?|[.,]\d+)$")


def validate_number(text, low, high):
    """Kiểm tra một ô số trong khoảng [low, high].

    Trả về (giá trị float, None) nếu hợp lệ, hoặc (None, thông báo lỗi).
    """
    text = (text or "").strip()
    if not NUMBER_RE.match(text):
        return None, "Vui lòng nhập một số."
    value = float(text.replace(",", "."))
    if value < low or value > high:
        return None, f"Giá trị phải từ {low} đến {high}."
    return value, None


def round1(value):
    """Làm tròn 1 chữ số thập phân."""
    return round(value, 1)


def classify(bmi):
    """Phân loại theo chuẩn người châu Á -> (nhãn, màu Bootstrap)."""
    if bmi < 18.5:
        return "Thiếu cân", "warning"
    if bmi < 23:
        return "Bình thường", "success"
    if bmi < 25:
        return "Thừa cân", "warning"
    return "Béo phì", "danger"


def healthy_weight_range(height_cm):
    """Cân nặng ứng với BMI 18,5 – 22,9."""
    h2 = (height_cm / 100) ** 2
    return round1(h2 * 18.5), round1(h2 * 22.9)


@app.route("/", methods=["GET", "POST"])
def index():
    form = {"cao": "", "nang": ""}
    errors = {}
    result = None

    if request.method == "POST":
        form["cao"] = request.form.get("cao", "").strip()
        form["nang"] = request.form.get("nang", "").strip()

        cao, error = validate_number(form["cao"], 50, 250)
        if error:
            # Gợi ý nếu người dùng nhập mét thay vì cm (ví dụ 1.7)
            if NUMBER_RE.match(form["cao"]) and float(form["cao"].replace(",", ".")) < 10:
                error += " (Nhập chiều cao bằng cm, không phải mét.)"
            errors["cao"] = f"Lỗi ô chiều cao: {error}"

        nang, error = validate_number(form["nang"], 10, 300)
        if error:
            errors["nang"] = f"Lỗi ô cân nặng: {error}"

        if not errors:
            bmi = round1(nang / ((cao / 100) ** 2))
            label, color = classify(bmi)
            low, high = healthy_weight_range(cao)
            result = {
                "text": f"{bmi:.1f} · {label}",
                "color": color,
                "range": f"Cân nặng nên có: {low:.1f} – {high:.1f} kg",
            }

    return render_template("index2.html", form=form, errors=errors, result=result)


if __name__ == "__main__":
    app.run(debug=True)