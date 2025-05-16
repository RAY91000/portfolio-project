import sqlite3

def print_table(cursor, table_name):
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        if not rows:
            print(f"\nTable '{table_name}' est vide.")
            return

        print(f"\nContenu de la table '{table_name}':")
        for row in rows:
            print(row)

    except sqlite3.OperationalError as e:
        print(f"\nErreur : {e} (table '{table_name}' introuvable ?)")

def main():
    db_path = "instance/app.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    tables = ["users", "challenges", "reviews", "submissions"]
    for table in tables:
        print_table(cursor, table)

    conn.close()

if __name__ == "__main__":
    main()
