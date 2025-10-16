import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_FILE = "data.json"

# ===== JSON操作 =====
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

# ===== 登録処理 =====
def add_user():
    name = entry_name.get().strip()
    if not name:
        messagebox.showwarning("警告", "名前を入力してください。")
        return

    data = load_data()
    new_id = max([user["id"] for user in data], default=0) + 1
    data.append({"id": new_id, "name": name})
    save_data(data)
    entry_name.delete(0, tk.END)
    update_listbox()
    messagebox.showinfo("登録完了", f"ID={new_id} で登録しました。")

# ===== 一覧更新 =====
def update_listbox():
    listbox.delete(0, tk.END)
    data = load_data()
    for user in data:
        listbox.insert(tk.END, f"ID={user['id']} | {user['name']}")

# ===== 削除処理 =====
def delete_user():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("警告", "削除する項目を選択してください。")
        return

    index = selection[0]
    data = load_data()
    if index >= len(data):
        messagebox.showerror("エラー", "選択が無効です。")
        return

    user = data[index]
    confirm = messagebox.askyesno("確認", f"ID={user['id']} | {user['name']} を削除しますか？")
    if confirm:
        data.pop(index)
        save_data(data)
        update_listbox()
        messagebox.showinfo("削除完了", "データを削除しました。")

# ===== GUI構築 =====
root = tk.Tk()
root.title("ユーザー管理ツール")
root.geometry("400x400")

# 入力エリア
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

label_name = tk.Label(frame_top, text="氏名:")
label_name.pack(side=tk.LEFT, padx=5)

entry_name = tk.Entry(frame_top, width=25)
entry_name.pack(side=tk.LEFT, padx=5)

btn_add = tk.Button(frame_top, text="登録", command=add_user)
btn_add.pack(side=tk.LEFT, padx=5)

# 一覧
label_list = tk.Label(root, text="登録一覧")
label_list.pack()

listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=5)

# 削除ボタン
btn_delete = tk.Button(root, text="選択項目を削除", command=delete_user)
btn_delete.pack(pady=10)

# 初期表示
update_listbox()

root.mainloop()
