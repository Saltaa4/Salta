from connect import connect
import re

conn = connect()
cur = conn.cursor()


def normalize_phone(phone):
    phone = phone.strip()
    phone = re.sub(r"[^\d+]", "", phone)

    if re.fullmatch(r"8\d{10}", phone):
        return "+7" + phone[1:]

    if re.fullmatch(r"\+7\d{10}", phone):
        return phone

    return None


def create_table():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook(
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    )
    """)
    conn.commit()
    print("Table ready")


def search_contacts():
    pattern = input("Enter search pattern: ").strip()

    cur.execute(
        "SELECT * FROM search_contacts(%s)",
        (pattern,)
    )
    rows = cur.fetchall()

    print("\nSearch result:")
    for row in rows:
        print(row)


def insert_or_update_user():
    name = input("Enter name: ").strip()
    phone_input = input("Enter phone: (+7XXXXXXXXXX or 8XXXXXXXXXX): ").strip()

    phone = normalize_phone(phone_input)

    if phone is None:
        print("Invalid phone format. Use +7XXXXXXXXXX or 8XXXXXXXXXX")
        return

    cur.execute(
        "CALL insert_or_update_user(%s, %s)",
        (name, phone)
    )
    conn.commit()
    print("Added or updated")


def show_paginated_contacts():
    limit = int(input("Enter limit: ").strip())
    offset = int(input("Enter offset: ").strip())

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s::INT, %s::INT)",
        (limit, offset)
    )
    rows = cur.fetchall()

    print("\nPaginated contacts:")
    for row in rows:
        print(row)


def delete_contact():
    value = input("Enter username or phone to delete: ").strip()

    normalized = normalize_phone(value)
    if normalized is not None:
        value = normalized

    cur.execute(
        "CALL delete_contact_by_value(%s::VARCHAR)",
        (value,)
    )
    conn.commit()
    print("Deleted")


def menu():
    create_table()

    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Search contacts by pattern")
        print("2. Insert or update user")
        print("3. Show paginated contacts")
        print("4. Delete contact by username or phone")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            search_contacts()
        elif choice == "2":
            insert_or_update_user()
        elif choice == "3":
            show_paginated_contacts()
        elif choice == "4":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


menu()

cur.close()
conn.close()
print("Connection closed")