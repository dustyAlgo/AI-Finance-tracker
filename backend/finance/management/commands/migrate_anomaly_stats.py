import pickle
import pyodbc
from django.core.management.base import BaseCommand
from pathlib import Path


class Command(BaseCommand):
    help = "Migrate anomaly stats from .pkl to Azure SQL"

    def handle(self, *args, **options):
        # Path to pickle file
        stats_path = Path("finance/ml/models/anomaly_stats.pkl")

        if not stats_path.exists():
            self.stdout.write(self.style.ERROR("Stats file not found"))
            return

        # Load pickle
        with open(stats_path, "rb") as f:
            stats = pickle.load(f)

        self.stdout.write("Loaded stats from pickle.")

        # Azure SQL connection details
        server = "financetrack-sql-server.database.windows.net"
        database = "finance-anomaly-db"
        username = "sqladmin"
        password = "Idontknow@123"

        conn_str = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password}"
        )

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        inserted = 0

        for user_id, categories in stats.items():
            for category_id, values in categories.items():
                mean = values["mean"]
                std = values["std"]
                count = values["count"]

                cursor.execute("""
                    INSERT INTO anomaly_stats
                    (user_id, category_id, mean, std_dev, sample_count)
                    VALUES (?, ?, ?, ?, ?)
                """, user_id, category_id, mean, std, count)

                inserted += 1

        conn.commit()
        conn.close()

        self.stdout.write(
            self.style.SUCCESS(f"Inserted {inserted} anomaly stat rows.")
        )
