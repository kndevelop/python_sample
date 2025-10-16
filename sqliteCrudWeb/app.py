from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3
import os

# Flask アプリ生成
app = Flask(__name__)

# DB ファイル名
DB_FILE = 'example.db'

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    # 行を dict 風に扱えるようにする（キーで参照可能に）
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """最初に一度だけ呼ぶ：schema.sql を使ってテーブルを作る"""
    if not os.path.exists(DB_FILE):
        conn = get_connection()
        with open('schema.sql', 'r', encoding='utf-8') as f:
            schema = f.read()
        conn.executescript(schema)
        conn.commit()
        conn.close()

@app.route('/')
def index():
    """ユーザー一覧表示"""
    conn = get_connection()
    cur = conn.execute("SELECT * FROM users ORDER BY id")
    users = cur.fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """ユーザー追加フォーム／処理"""
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
    """ユーザー編集フォーム／処理"""
    conn = get_connection()
    cur = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    if user is None:
        conn.close()
        abort(404)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        if not name:
            conn.close()
            return "名前を入力してください", 400
        try:
            age_i = int(age) if age != '' else None
        except ValueError:
            conn.close()
            return "年齢は整数で入力してください", 400

        conn.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (name, age_i, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        conn.close()
        return render_template('edit.html', user=user)

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    """ユーザー削除処理"""
    conn = get_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)