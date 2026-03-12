from pathlib import Path

from flask import Flask, redirect, send_from_directory

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent


@app.route("/favicon.ico")
def favicon():
    """Отдаём иконку для браузера, чтобы не было 404."""
    return send_from_directory(BASE_DIR / "static", "favicon.png")


@app.route("/")
def index():
    """Главная: редирект на страницу поиска кабинета."""
    return redirect("/info")


@app.route("/info")
def info():
    """Страница поиска по имени."""
    return send_from_directory(BASE_DIR, "info.html")


@app.route("/dashbord")
def dashbord():
    """Большой дашборд для экрана на этаже."""
    return send_from_directory(BASE_DIR, "dashbord.html")


@app.route("/mobile-dashbord")
def mobile_dashbord():
    """Мобильная версия дашборда с поиском."""
    return send_from_directory(BASE_DIR, "mobile-dashbord.html")


@app.route("/show-iskra")
def show_iskra():
    """Страница с таймером до начала шоу."""
    return send_from_directory(BASE_DIR, "show-iskra.html")


@app.route("/admin-show")
def admin_show():
    """Админ-панель для принудительного запуска шоу."""
    return send_from_directory(BASE_DIR, "admin-show.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)