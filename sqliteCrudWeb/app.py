from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'example.db'

# -------------------------
# データベース初期化
# -------------------------
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        with open('schema.sql', 'r', encoding='utf-8') as f:
            schema = f.read()
        conn.executescript(schema)
        conn.commit()
        conn.close()

# -------------------------
# DB接続
# -------------------------
def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------
# ルーティング
# -------------------------
@app.route('/')
def index():
    conn = get_connection()
    cur = conn.execute("SELECT * FROM users ORDER BY id")
    users = cur.fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        if not name:
            return "名前を入力してください", 400
        try:
            age_i = int(age) if age != '' else None
        except ValueError:
            return "年齢は整数で入力してください", 400

        conn = get_connection()
        conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age_i))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        return render_template('form.html')

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    conn = get_connection()
    cur = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    if not user:
        conn.close()
        abort(404)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        if not name:
            conn.close()
            return "名前を入力してください", 400
        age_i = int(age) if age else None

        conn.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (name, age_i, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        conn.close()
        return render_template('edit.html', user=user)

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    conn = get_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# -------------------------
# アプリ起動
# -------------------------
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)