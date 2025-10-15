from flask import Flask, render_template, request, redirect, jsonify
import json, os

app = Flask(__name__)
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", users=data)

@app.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"].strip()
    if name:
        data = load_data()
        new_id = max([u["id"] for u in data], default=0) + 1
        data.append({"id": new_id, "name": name})
        save_data(data)
    return redirect("/")

@app.route("/delete/<int:user_id>")
def delete_user(user_id):
    data = load_data()
    data = [u for u in data if u["id"] != user_id]
    save_data(data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)