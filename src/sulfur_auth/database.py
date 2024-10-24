import os
import csv


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        if not os.path.exists(db_name):
            os.makedirs(db_name)

    def _get_table_path(self, table_name):
        return os.path.join(self.db_name, f"{table_name}.csv")

    def create_table(self, table_name, columns):
        table_path = self._get_table_path(table_name)
        if os.path.exists(table_path):
            os.remove(table_path)
        with open(table_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(columns)  # Write column headers

    def insert(self, table_name, data):
        table_path = self._get_table_path(table_name)
        if not os.path.exists(table_path):
            raise Exception(f"Table {table_name} does not exist.")

        with open(table_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def select(self, table_name, conditions=None):
        table_path = self._get_table_path(table_name)
        if not os.path.exists(table_path):
            raise Exception(f"Table {table_name} does not exist.")

        results = []
        with open(table_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if conditions:
                    # Apply conditions if provided (like where clause)
                    if all(row[col] == str(val) for col, val in conditions.items()):
                        results.append(row)
                else:
                    results.append(row)

        return results

    def update(self, table_name, conditions, new_data):
        table_path = self._get_table_path(table_name)
        if not os.path.exists(table_path):
            raise Exception(f"Table {table_name} does not exist.")

        updated = False
        rows = []
        with open(table_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if all(row[col] == str(val) for col, val in conditions.items()):
                    for key, val in new_data.items():
                        row[key] = str(val)
                    updated = True
                rows.append(row)

        # Rewrite the file with updated data
        with open(table_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        return updated

    def delete(self, table_name, conditions):
        table_path = self._get_table_path(table_name)
        if not os.path.exists(table_path):
            raise Exception(f"Table {table_name} does not exist.")

        deleted = False
        rows = []
        with open(table_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if all(row[col] == str(val) for col, val in conditions.items()):
                    deleted = True  # Skip rows that match the conditions (delete)
                else:
                    rows.append(row)

        # Rewrite the file without the deleted rows
        with open(table_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        return deleted
