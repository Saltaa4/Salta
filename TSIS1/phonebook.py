import csv
import json
import re
from connect import get_connection


def normalize_phone(phone):
    phone = re.sub(r"[^\d+]", "", phone.strip())
    if re.fullmatch(r"8\d{10}", phone):
        return "+7" + phone[1:]
    if re.fullmatch(r"\+7\d{10}", phone):
        return phone
    return None


def get_group_id(cur, group_name):
    cur.execute(
        "INSERT INTO groups(name) VALUES(%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )

    cur.execute(
        "SELECT id FROM groups WHERE name = %s",
        (group_name,)
    )

    return cur.fetchone()[0]


def print_rows(rows):
    if not rows:
        print("Nothing found.")
        return

    for row in rows:
        print(
            f"Name: {row[0]} | Email: {row[1]} | Birthday: {row[2]} | "
            f"Group: {row[3]} | Phone: {row[4]} ({row[5]})"
        )


def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_name = input("Group (Family/Work/Friend/Other): ")

    # ── normalize_phone ──
    phone_raw = input("Phone (+7XXXXXXXXXX or 8XXXXXXXXXX): ")
    phone = normalize_phone(phone_raw)
    if phone is None:
        print("Invalid phone format. Use +7XXXXXXXXXX or 8XXXXXXXXXX")
        return
    # ────────────────────

    phone_type = input("Phone type (home/work/mobile): ")

    conn = get_connection()

    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cur:
                group_id = get_group_id(cur, group_name)

                cur.execute(
                    """
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (name) DO UPDATE
                    SET email = EXCLUDED.email,
                        birthday = EXCLUDED.birthday,
                        group_id = EXCLUDED.group_id
                    RETURNING id
                    """,
                    (name, email, birthday, group_id)
                )

                contact_id = cur.fetchone()[0]

                cur.execute(
                    """
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (phone) DO NOTHING
                    """,
                    (contact_id, phone, phone_type)
                )

        print("Contact added successfully!")

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


def show_contacts():
    conn = get_connection()

    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    c.name,
                    c.email,
                    c.birthday,
                    g.name,
                    p.phone,
                    p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                ORDER BY c.name
                """
            )

            rows = cur.fetchall()
            print("\n--- Contacts ---")
            print_rows(rows)

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


def add_phone():
    name = input("Contact name: ")

    # ── normalize_phone ──
    phone_raw = input("New phone (+7XXXXXXXXXX or 8XXXXXXXXXX): ")
    phone = normalize_phone(phone_raw)
    if phone is None:
        print("Invalid phone format. Use +7XXXXXXXXXX or 8XXXXXXXXXX")
        return
    # ────────────────────

    phone_type = input("Phone type (home/work/mobile): ")

    conn = get_connection()

    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL add_phone(%s, %s, %s)",
                    (name, phone, phone_type)
                )

        print("Phone added!")

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


def move_to_group():
    name = input("Contact name: ")
    group_name = input("New group: ")

    conn = get_connection()

    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL move_to_group(%s, %s)",
                    (name, group_name)
                )

        print("Contact moved to group!")

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


def search_contacts():
    query = input("Search by name/email/phone/group: ")

    conn = get_connection()

    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM search_contacts(%s)",
                (query,)
            )

            rows = cur.fetchall()
            print("\n--- Search results ---")
            print_rows(rows)

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


def filter_by_group():
    group_name = input("Group name: ")

    conn = get_connection()

    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    c.name,
                    c.email,
                    c.birthday,
                    g.name,
                    p.phone,
                    p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                WHERE g.name ILIKE %s
                ORDER BY c.name
                """,
                ("%" + group_name + "%",)
            )

            rows = cur.fetchall()
            print("\n--- Group filter results ---")
            print_rows(rows)

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


def search_by_email():
    email_part = input("Email search: ")

    conn = get_connection()

    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    c.name,
                    c.email,
                    c.birthday,
                    g.name,
                    p.phone,
                    p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                WHERE c.email ILIKE %s
                ORDER BY c.name
                """,
                ("%" + email_part + "%",)
            )

            rows = cur.fetchall()
            print("\n--- Email search results ---")
            print_rows(rows)

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


def sort_contacts():
    print("Sort by:")
    print("1 - name")
    print("2 - birthday")
    print("3 - date added")

    choice = input("Choose: ")

    if choice == "1":
        order_by = "c.name"
    elif choice == "2":
        order_by = "c.birthday"
    elif choice == "3":
        order_by = "c.created_at"
    else:
        print("Invalid choice")
        return

    conn = get_connection()

    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT
                    c.name,
                    c.email,
                    c.birthday,
                    g.name,
                    p.phone,
                    p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                ORDER BY {order_by}
                """
            )

            rows = cur.fetchall()
            print("\n--- Sorted contacts ---")
            print_rows(rows)

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


def paginated_navigation():
    limit = int(input("Page size: ") or 5)
    page = 0

    while True:
        offset = page * limit

        conn = get_connection()

        if not conn:
            return

        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_paginated(%s, %s)",
                    (limit, offset)
                )

                rows = cur.fetchall()

                print(f"\n--- Page {page + 1} ---")
                print_rows(rows)

        except Exception as error:
            print("Error:", error)

        finally:
            conn.close()

        command = input("\nn - next, p - previous, q - quit: ")

        if command == "n":
            page += 1
        elif command == "p":
            if page > 0:
                page -= 1
        elif command == "q":
            break
        else:
            print("Invalid command")


def export_to_json():
    filename = input("JSON filename to export: ") or "contacts.json"

    conn = get_connection()

    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    c.id,
                    c.name,
                    c.email,
                    c.birthday,
                    g.name
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                ORDER BY c.name
                """
            )

            contacts = cur.fetchall()
            result = []

            for contact in contacts:
                contact_id, name, email, birthday, group_name = contact

                cur.execute(
                    """
                    SELECT phone, type
                    FROM phones
                    WHERE contact_id = %s
                    """,
                    (contact_id,)
                )

                phones = cur.fetchall()

                result.append({
                    "name": name,
                    "email": email,
                    "birthday": str(birthday) if birthday else None,
                    "group": group_name,
                    "phones": [
                        {"phone": phone[0], "type": phone[1]}
                        for phone in phones
                    ]
                })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

        print("Exported to", filename)

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


def import_from_json():
    filename = input("JSON filename to import: ") or "contacts.json"

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

    except Exception as error:
        print("File error:", error)
        return

    conn = get_connection()

    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cur:
                for item in data:
                    name = item["name"]
                    email = item.get("email")
                    birthday = item.get("birthday")
                    group_name = item.get("group", "Other")
                    phones = item.get("phones", [])

                    cur.execute(
                        "SELECT id FROM contacts WHERE name = %s",
                        (name,)
                    )

                    existing = cur.fetchone()

                    if existing:
                        action = input(f"{name} already exists. skip or overwrite? ")

                        if action.lower() == "skip":
                            continue

                        elif action.lower() == "overwrite":
                            contact_id = existing[0]
                            group_id = get_group_id(cur, group_name)

                            cur.execute(
                                """
                                UPDATE contacts
                                SET email = %s,
                                    birthday = %s,
                                    group_id = %s
                                WHERE id = %s
                                """,
                                (email, birthday, group_id, contact_id)
                            )

                            cur.execute(
                                "DELETE FROM phones WHERE contact_id = %s",
                                (contact_id,)
                            )

                        else:
                            print("Invalid action. Skipped.")
                            continue

                    else:
                        group_id = get_group_id(cur, group_name)

                        cur.execute(
                            """
                            INSERT INTO contacts(name, email, birthday, group_id)
                            VALUES (%s, %s, %s, %s)
                            RETURNING id
                            """,
                            (name, email, birthday, group_id)
                        )

                        contact_id = cur.fetchone()[0]

                    for phone_item in phones:
                        cur.execute(
                            """
                            INSERT INTO phones(contact_id, phone, type)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (phone) DO NOTHING
                            """,
                            (contact_id, phone_item["phone"], phone_item["type"])
                        )

        print("JSON import completed!")

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


def import_from_csv():
    filename = input("CSV filename: ") or "contacts.csv"

    conn = get_connection()

    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cur:
                with open(filename, "r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)

                    for row in reader:
                        name = row["name"]
                        email = row["email"]
                        birthday = row["birthday"]
                        group_name = row["group"]
                        phone_type = row["type"]

                        # ── normalize_phone ──
                        phone_raw = row["phone"]
                        phone = normalize_phone(phone_raw)
                        if phone is None:
                            print(f"Skipping invalid phone '{phone_raw}' for {name}")
                            continue
                        # ────────────────────

                        group_id = get_group_id(cur, group_name)

                        cur.execute(
                            """
                            INSERT INTO contacts(name, email, birthday, group_id)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (name) DO UPDATE
                            SET email = EXCLUDED.email,
                                birthday = EXCLUDED.birthday,
                                group_id = EXCLUDED.group_id
                            RETURNING id
                            """,
                            (name, email, birthday, group_id)
                        )

                        contact_id = cur.fetchone()[0]

                        cur.execute(
                            """
                            INSERT INTO phones(contact_id, phone, type)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (phone) DO NOTHING
                            """,
                            (contact_id, phone, phone_type)
                        )

        print("CSV import completed!")

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


def delete_contact():
    value = input("Name or phone to delete: ")

    conn = get_connection()

    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL delete_contact_by_value(%s)",
                    (value,)
                )

        print("Contact deleted!")

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


def update_phone():
    name = input("Contact name: ")
    old_phone = input("Old phone: ")
    new_phone = input("New phone: ")
    new_type = input("New phone type (home/work/mobile): ")

    conn = get_connection()

    if not conn:
        return

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE phones
                    SET phone = %s,
                        type = %s
                    WHERE phone = %s
                      AND contact_id = (
                          SELECT id FROM contacts
                          WHERE name = %s
                          LIMIT 1
                      )
                    """,
                    (new_phone, new_type, old_phone, name)
                )

                if cur.rowcount == 0:
                    print("Phone not found.")
                else:
                    print("Phone updated successfully!")

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


def main():
    while True:
        print("\n--- TSIS1 EXTENDED PHONEBOOK ---")
        print("1 - Add contact")
        print("2 - Show contacts")
        print("3 - Add phone to contact")
        print("4 - Move contact to group")
        print("5 - Search contacts")
        print("6 - Filter by group")
        print("7 - Search by email")
        print("8 - Sort contacts")
        print("9 - Paginated navigation")
        print("10 - Export to JSON")
        print("11 - Import from JSON")
        print("12 - Import from CSV")
        print("13 - Delete contact")
        print("14 - Update phone")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            add_phone()
        elif choice == "4":
            move_to_group()
        elif choice == "5":
            search_contacts()
        elif choice == "6":
            filter_by_group()
        elif choice == "7":
            search_by_email()
        elif choice == "8":
            sort_contacts()
        elif choice == "9":
            paginated_navigation()
        elif choice == "10":
            export_to_json()
        elif choice == "11":
            import_from_json()
        elif choice == "12":
            import_from_csv()
        elif choice == "13":
            delete_contact()
        elif choice == "14":
            update_phone()
        elif choice == "0":
            print("Good bye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()