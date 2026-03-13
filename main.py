from pathlib import Path
from flask import Flask, redirect, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'leonardo_secret_1409'
socketio = SocketIO(app, cors_allowed_origins="*")

BASE_DIR = Path(__file__).resolve().parent

# --- State for Real-Time Features ---
# In a real app, this would be in a database.
state = {
    "video_link": "https://vk.com/video_ext.php?oid=-202041326&id=456242024&hd=2&autoplay=1&t=3347",
    "chat_messages": [
        {"id": "msg_0", "author": "Модератор", "text": "Добро пожаловать на трансляцию конкурса «Леонардо»! Задавайте свои вопросы здесь.", "is_moderator": True}
    ],
    "viewer_count": 0
}

# --- SocketIO Events ---

@socketio.on('connect')
def handle_connect():
    state["viewer_count"] += 1
    # Send current state to the new client
    emit('init_state', {
        'video_link': state['video_link'],
        'chat_messages': state['chat_messages']
    })
    # Update everyone's viewer count
    emit('viewer_count_updated', {'count': state["viewer_count"]}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    state["viewer_count"] = max(0, state["viewer_count"] - 1)
    emit('viewer_count_updated', {'count': state["viewer_count"]}, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    import uuid
    new_msg = {
        "id": str(uuid.uuid4()),
        "author": data.get("author", "Гость"),
        "text": data.get("text", ""),
        "is_moderator": data.get("is_moderator", False)
    }
    state["chat_messages"].append(new_msg)
    # Keep only last 100 messages
    if len(state["chat_messages"]) > 100:
        state["chat_messages"].pop(0)
    
    emit('new_message', new_msg, broadcast=True)

@socketio.on('delete_message')
def handle_delete_message(data):
    msg_id = data.get("id")
    state["chat_messages"] = [m for m in state["chat_messages"] if m["id"] != msg_id]
    emit('message_deleted', {'id': msg_id}, broadcast=True)

@socketio.on('update_video_link')
def handle_update_video(data):
    new_link = data.get("link")
    if new_link:
        state["video_link"] = new_link
        emit('video_link_updated', {'link': new_link}, broadcast=True)

@socketio.on('send_overlay_message')
def handle_overlay_message(data):
    # Broadcast overlay message to all clients
    emit('overlay_message', {'text': data.get("text")}, broadcast=True)

# --- Routes ---


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


@app.route("/tv")
def tv():
    "Страница TV"
    return send_from_directory(BASE_DIR, "tv.html")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)