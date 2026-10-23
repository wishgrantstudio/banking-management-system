import os

import mysql.connector
from flask import Flask, render_template_string

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

        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Banking Management System</title>

            <style>
                * {
                    box-sizing: border-box;
                }

                body {
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background: #f2f5f9;
                    color: #1f2937;
                }

                header {
                    background: #12305a;
                    color: white;
                    padding: 22px 6%;
                }

                header h1 {
                    margin: 0;
                }

                header p {
                    margin-bottom: 0;
                    color: #dbeafe;
                }

                main {
                    width: 88%;
                    max-width: 1200px;
                    margin: 30px auto;
                }

                .cards {
                    display: grid;
                    grid-template-columns: repeat(
                        auto-fit, minmax(210px, 1fr)
                    );
                    gap: 20px;
                    margin-bottom: 30px;
                }

                .card {
                    background: white;
                    padding: 24px;
                    border-radius: 12px;
                    box-shadow: 0 3px 12px #0000000d;
                }

                .card h3 {
                    margin-top: 0;
                    color: #64748b;
                    font-size: 15px;
                }

                .card .number {
                    font-size: 28px;
                    font-weight: bold;
                    color: #12305a;
                }

                .table-container {
                    overflow-x: auto;
                    background: white;
                    padding: 22px;
                    border-radius: 12px;
                    box-shadow: 0 3px 12px #0000000d;
                }

                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 15px;
                }

                th, td {
                    padding: 13px;
                    text-align: left;
                    border-bottom: 1px solid #e5e7eb;
                    white-space: nowrap;
                }

                th {
                    background: #eef3f9;
                    color: #12305a;
                }

                .status {
                    text-transform: capitalize;
                }

                footer {
                    text-align: center;
                    padding: 20px;
                    color: #64748b;
                }

                @media (max-width: 600px) {
                    main {
                        width: 94%;
                    }

                    header {
                        padding: 20px 3%;
                    }
                }
            </style>
        </head>

        <body>
            <header>
                <h1>Banking Management System</h1>
                <p>Dashboard — Account and Customer Overview</p>
            </header>

            <main>
                <section class="cards">
                    <div class="card">
                        <h3>Total Customers</h3>
                        <div class="number">{{ total_customers }}</div>
                    </div>

                    <div class="card">
                        <h3>Total Accounts</h3>
                        <div class="number">{{ total_accounts }}</div>
                    </div>

                    <div class="card">
                        <h3>Total Account Balance</h3>
                        <div class="number">
                            ₹{{ "{:,.2f}".format(total_balance) }}
                        </div>
                    </div>
                </section>

                <section class="table-container">
                    <h2>Customer Accounts</h2>

                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Customer</th>
                                <th>Email</th>
                                <th>Account Number</th>
                                <th>Type</th>
                                <th>Balance</th>
                                <th>Status</th>
                            </tr>
                        </thead>

                        <tbody>
                            {% for account in accounts %}
                            <tr>
                                <td>{{ account.customer_id }}</td>
                                <td>{{ account.customer_name }}</td>
                                <td>{{ account.email }}</td>
                                <td>{{ account.account_number }}</td>
                                <td>{{ account.account_type }}</td>
                                <td>₹{{ "{:,.2f}".format(account.balance) }}</td>
                                <td class="status">{{ account.status }}</td>
                            </tr>
                            {% else %}
                            <tr>
                                <td colspan="7">No accounts found.</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </section>
            </main>

            <footer>
                Banking Management System | College Database Project
            </footer>
        </body>
        </html>
        """,
        total_customers=total_customers,
        total_accounts=total_accounts,
        total_balance=total_balance,
        accounts=accounts)

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
