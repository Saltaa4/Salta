import csv
from connect import get_connection


def create_table():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS phonebook (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(100) NOT NULL,
                        phone VARCHAR(20) NOT NULL UNIQUE
                    );
                """)
        print("Table created successfully.")
    except Exception as e:
        print(f"Error: {e}")


def insert_from_console():
    username = input("Enter username: ").strip()
    phone = input("Enter phone: ").strip()

    if not username or not phone:
        print("Empty values not allowed.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                    (username, phone)
                )
        print("Contact added.")
    except Exception as e:
        print(f"Error: {e}")


def insert_from_csv(filename="contacts.csv"):
    try:
        with open(filename, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            print("Detected columns:", reader.fieldnames)

            if not reader.fieldnames:
                print("CSV file is empty.")
                return

            fieldnames = [name.strip().lower() for name in reader.fieldnames]

            if "username" not in fieldnames or "phone" not in fieldnames:
                print("CSV must have 'username' and 'phone'")
                return

            file.seek(0)
            reader = csv.DictReader(file)

            with get_connection() as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        normalized = {}
                        for k, v in row.items():
                            clean_key = k.strip().lower().replace("\ufeff", "")
                            clean_value = v.strip() if v else ""
                            normalized[clean_key] = clean_value

                        if not normalized.get("username") or not normalized.get("phone"):
                            continue

                        cur.execute("""
                            INSERT INTO phonebook (username, phone)
                            VALUES (%s, %s)
                            ON CONFLICT (phone) DO NOTHING
                        """, (normalized["username"], normalized["phone"]))

        print("CSV data inserted.")

    except FileNotFoundError:
        print("CSV file not found.")
    except Exception as e:
        print(f"Error: {e}")


def query_all():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username, phone FROM phonebook ORDER BY id")
                rows = cur.fetchall()

                if not rows:
                    print("No data.")
                    return

                for row in rows:
                    print(f"Name: {row[0]} | Phone: {row[1]}")

    except Exception as e:
        print(f"Error: {e}")


def query_by_name():
    name = input("Enter name: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM phonebook WHERE username ILIKE %s",
                    (f"%{name}%",)
                )

                rows = cur.fetchall()

                if not rows:
                    print("No matches found.")
                    return

                for row in rows:
                    print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")

    except Exception as e:
        print(f"Error: {e}")


def query_by_phone_prefix():
    prefix = input("Enter prefix: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM phonebook WHERE phone LIKE %s",
                    (f"{prefix}%",)
                )

                rows = cur.fetchall()

                if not rows:
                    print("No matches found.")
                    return

                for row in rows:
                    print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")

    except Exception as e:
        print(f"Error: {e}")


def update_contact():
    phone = input("Enter existing phone: ").strip()
    new_username = input("New username (Enter to skip): ").strip()
    new_phone = input("New phone (Enter to skip): ").strip()

    if not new_username and not new_phone:
        print("Nothing to update.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if new_username and new_phone:
                    cur.execute(
                        "UPDATE phonebook SET username=%s, phone=%s WHERE phone=%s",
                        (new_username, new_phone, phone)
                    )
                elif new_username:
                    cur.execute(
                        "UPDATE phonebook SET username=%s WHERE phone=%s",
                        (new_username, phone)
                    )
                elif new_phone:
                    cur.execute(
                        "UPDATE phonebook SET phone=%s WHERE phone=%s",
                        (new_phone, phone)
                    )

                if cur.rowcount == 0:
                    print("No contact found.")
                else:
                    print("Contact updated.")

    except Exception as e:
        print(f"Error: {e}")


def delete_contact():
    username = input("Enter contact name to delete: ").strip()

    if not username:
        print("Name cannot be empty.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM phonebook WHERE username=%s", (username,))

                if cur.rowcount == 0:
                    print("No contact found.")
                else:
                    print("Contact deleted.")

    except Exception as e:
        print(f"Error: {e}")


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert from CSV")
        print("3. Insert from console")
        print("4. Show all contacts")
        print("5. Search by name")
        print("6. Search by phone prefix")
        print("7. Update contact")
        print("8. Delete contact")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            query_all()
        elif choice == "5":
            query_by_name()
        elif choice == "6":
            query_by_phone_prefix()
        elif choice == "7":
            update_contact()
        elif choice == "8":
            delete_contact()
        elif choice == "0":
            print("Exit.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()