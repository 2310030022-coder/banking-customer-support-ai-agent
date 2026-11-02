import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'banking_support.db'


def connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize():
    with connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS support_tickets (
          ticket_number TEXT PRIMARY KEY,
          customer_name TEXT NOT NULL,
          issue TEXT NOT NULL,
          status TEXT NOT NULL DEFAULT 'Unresolved',
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS interaction_logs (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          customer_name TEXT NOT NULL,
          message TEXT NOT NULL,
          classification TEXT NOT NULL,
          agent TEXT NOT NULL,
          response TEXT NOT NULL,
          ticket_number TEXT,
          created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )''')


def create_ticket(ticket_number, customer_name, issue):
    with connection() as conn:
        conn.execute('INSERT INTO support_tickets (ticket_number, customer_name, issue) VALUES (?, ?, ?)',
                     (ticket_number, customer_name, issue))


def get_ticket(ticket_number):
    with connection() as conn:
        row = conn.execute('SELECT * FROM support_tickets WHERE ticket_number = ?', (ticket_number,)).fetchone()
    return dict(row) if row else None


def record_interaction(customer_name, message, classification, agent, response, ticket_number=None):
    with connection() as conn:
        conn.execute('''INSERT INTO interaction_logs
             (customer_name, message, classification, agent, response, ticket_number)
             VALUES (?, ?, ?, ?, ?, ?)''',
             (customer_name, message, classification, agent, response, ticket_number))


def recent_logs(limit=50):
    with connection() as conn:
        rows = conn.execute('SELECT * FROM interaction_logs ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
    return [dict(row) for row in rows]


def recent_tickets(limit=50):
    with connection() as conn:
        rows = conn.execute('SELECT * FROM support_tickets ORDER BY created_at DESC LIMIT ?', (limit,)).fetchall()
    return [dict(row) for row in rows]
