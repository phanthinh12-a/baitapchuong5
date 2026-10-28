import re
from decimal import Decimal
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="index.html")
OPERATORS = ("+", "-", "*", "/")

NUMBER_RE = re.compile(r"^[+-]?(\d+([.,]\d*)?|[.,]\d+)$")


def parse_number(text):
    """Trả về Decimal nếu hợp lệ, ngược lại trả về None."""
    text = (text or "").strip()
    if not NUMBER_RE.match(text):
        return None
    return Decimal(text.replace(",", "."))


def fmt(value):
    """Định dạng số: 10 thay vì 10.0, 3.5, -2.5 ..."""
    value = round(value, 10)
    text = format(value.normalize(), "f")
    return "0" if text in ("-0", "") else text


@app.route("/", methods=["GET", "POST"])
def index():
    form = {"a": "", "op": "+", "b": ""}
    errors = {}
    result = None

    if request.method == "POST":
        form["a"] = request.form.get("a", "").strip()
        form["b"] = request.form.get("b", "").strip()
        form["op"] = request.form.get("op", "").strip()

        a = parse_number(form["a"])
        b = parse_number(form["b"])

        if a is None:
            errors["a"] = "Lỗi ô a: Vui lòng nhập một số."
        if b is None:
            errors["b"] = "Lỗi ô b: Vui lòng nhập một số."
        if form["op"] not in OPERATORS:
            errors["op"] = "Phép toán không hợp lệ."
        if not errors and form["op"] == "/" and b == 0:
            errors["b"] = "Lỗi ô b: Không thể chia cho 0."

        if not errors:
            op = form["op"]
            if op == "+":
                value = a + b
            elif op == "-":
                value = a - b
            elif op == "*":
                value = a * b
            else:
                value = a / b
            result = f"{fmt(a)} {op} {fmt(b)} = {fmt(value)}"

    return render_template(
        "index.html",
        form=form,
        errors=errors,
        result=result,
        operators=OPERATORS,
    )


if __name__ == "__main__":
    app.run(debug=True)