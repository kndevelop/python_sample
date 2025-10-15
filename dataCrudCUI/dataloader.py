import json
import os

DATA_FILE = "data.json"

# ====== JSONファイルの基本操作 ======

def load_data():
    """JSONファイルを読み込む"""
    if not os.path.exists(DATA_FILE):
        return []  # ファイルがなければ空のリストを返す
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []  # 中身が壊れていたら空にする

def save_data(data):
    """JSONファイルに書き込む"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ====== 機能 ======

def add_user():
    """氏名を入力して登録"""
    name = input("氏名を入力してください: ").strip()
    if not name:
        print("名前が空です。登録を中止します。")
        return
    data = load_data()
    # IDは自動採番（最大ID + 1）
    new_id = (max([user["id"] for user in data], default=0) + 1)
    data.append({"id": new_id, "name": name})
    save_data(data)
    print(f"✅ 登録しました: ID={new_id}, 氏名={name}")

def list_users():
    """登録済みユーザー一覧を表示"""
    data = load_data()
    if not data:
        print("登録データがありません。")
        return
    print("\n📋 登録一覧:")
    for user in data:
        print(f"  ID={user['id']} | 氏名={user['name']}")
    print()

def delete_user():
    """IDを指定して削除"""
    try:
        target_id = int(input("削除したいIDを入力してください: "))
    except ValueError:
        print("❌ 数字で入力してください。")
        return

    data = load_data()
    new_data = [user for user in data if user["id"] != target_id]

    if len(new_data) == len(data):
        print("❌ 該当IDが見つかりません。")
        return

    save_data(new_data)
    print(f"🗑️ ID={target_id} のデータを削除しました。")

# ====== メインメニュー ======

def main():
    while True:
        print("\n=== メニュー ===")
        print("1. 登録")
        print("2. 一覧表示")
        print("3. 削除")
        print("4. 終了")

        choice = input("番号を選んでください: ").strip()
        if choice == "1":
            add_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            delete_user()
        elif choice == "4":
            print("終了します。")
            break
        else:
            print("無効な選択です。")

if __name__ == "__main__":
    main()
