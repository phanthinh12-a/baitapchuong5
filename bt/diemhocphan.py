import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from flask import Flask, render_template, request

# Thư mục chứa file HTML: D:\bt chuong 5\html
HTML_DIR = Path(__file__).resolve().parent.parent / "html"

app = Flask(__name__, template_folder=str(HTML_DIR))


FIELDS = (
    ("cc", "CC", Decimal("0.1")),
    ("gk", "GK", Decimal("0.3")),
    ("ck", "CK", Decimal("0.6")),
)

NUMBER_RE = re.compile(r"^[+-]?(\d+([.,]\d*)?|[.,]\d+)$")


def validate_score(text):
    """Hàm kiểm tra dùng chung cho cả 3 ô.

    Trả về (giá trị Decimal, None) nếu hợp lệ,
    hoặc (None, thông báo lỗi) nếu không hợp lệ.
    """
    text = (text or "").strip()
    if not NUMBER_RE.match(text):
        return None, "Vui lòng nhập một số."
    value = Decimal(text.replace(",", "."))
    if value < 0 or value > 10:
        return None, "Điểm phải từ 0 đến 10."
    return value, None


def letter_grade(score):
    if score >= Decimal("8.5"):
        return "A"
    if score >= Decimal("7.0"):
        return "B"
    if score >= Decimal("5.5"):
        return "C"
    if score >= Decimal("4.0"):
        return "D"
    return "F"


def calculate(cc, gk, ck):
    """Trả về (điểm học phần đã làm tròn 1 chữ số, điểm chữ, ghi chú)."""
    total = cc * Decimal("0.1") + gk * Decimal("0.3") + ck * Decimal("0.6")
    total = total.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

    if ck < 1:
        return total, "F", "điểm thi dưới 1"
    return total, letter_grade(total), None


@app.route("/", methods=["GET", "POST"])
def index():
    form = {key: "" for key, _, _ in FIELDS}
    errors = {}
    result = None

    if request.method == "POST":
        values = {}
        for key, label, _ in FIELDS:
            form[key] = request.form.get(key, "")
            value, error = validate_score(form[key])
            if error:
                errors[key] = f"Lỗi ô {label}: {error}"
            else:
                values[key] = value

        if not errors:
            total, grade, note = calculate(values["cc"], values["gk"], values["ck"])
            result = f"{total} · {grade}"
            if note:
                result += f" ({note})"

    return render_template("index1.html", form=form, errors=errors, result=result)


if __name__ == "__main__":
    app.run(debug=True)