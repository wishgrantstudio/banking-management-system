import os

import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"]
    )


@app.route("/")
def home():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Get dashboard statistics
        cursor.execute("SELECT COUNT(*) AS total_customers FROM customers")
        total_customers = cursor.fetchone()["total_customers"]

        cursor.execute("SELECT COUNT(*) AS total_accounts FROM accounts")
        total_accounts = cursor.fetchone()["total_accounts"]

        cursor.execute("""
            SELECT COALESCE(SUM(balance), 0) AS total_balance
            FROM accounts
        """)
        total_balance = cursor.fetchone()["total_balance"]

        # Get customer and account details
        cursor.execute("""
            SELECT
                c.customer_id,
                CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
                c.email,
                a.account_number,
                a.account_type,
                a.balance,
                a.status
            FROM customers AS c
            JOIN accounts AS a
                ON c.customer_id = a.customer_id
            ORDER BY c.customer_id
        """)

        accounts = cursor.fetchall()

        return render_template(
            "dashboard.html",
            total_customers=total_customers,
            total_accounts=total_accounts,
            total_balance=total_balance,
            accounts=accounts
        )

    except (mysql.connector.Error, KeyError):
        app.logger.exception("Dashboard error")
        return "Unable to load dashboard. Check the Flask terminal.", 500

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)
