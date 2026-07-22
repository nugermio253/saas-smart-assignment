import sqlite3
import os

DB = "state/round_robin.db"


class RoundRobinDB:

    def __init__(self):

        os.makedirs("state", exist_ok=True)

        conn = self.connect()

        conn.execute("""
            CREATE TABLE IF NOT EXISTS state(
                id INTEGER PRIMARY KEY,
                last_agent INTEGER
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS assignments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER,
                ticket_number TEXT,
                ticket_title TEXT,
                customer_id INTEGER,
                customer_name TEXT,
                organization_id INTEGER,
                organization_name TEXT,
                group_id INTEGER,
                group_name TEXT,
                priority_id INTEGER,
                priority_name TEXT,
                state_id INTEGER,
                state_name TEXT,
                agent_id INTEGER,
                agent_name TEXT,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    ############################################################

    def connect(self):

        conn = sqlite3.connect(DB)

        conn.row_factory = sqlite3.Row

        return conn

    ############################################################
    # ROUND ROBIN
    ############################################################

    def get_last_agent(self):

        conn = self.connect()

        c = conn.cursor()

        c.execute("""
            SELECT last_agent
            FROM state
            WHERE id=1
        """)

        row = c.fetchone()

        conn.close()

        if row:
            return row["last_agent"]

        return None

    ############################################################

    def save_last_agent(self, agent):

        conn = self.connect()

        conn.execute("""
            INSERT OR REPLACE INTO state(id,last_agent)
            VALUES(1,?)
        """, (agent,))

        conn.commit()

        conn.close()

    ############################################################
    # REGISTAR ATRIBUIÇÃO
    ############################################################

    def register_assignment(self, ticket, agent):

        conn = self.connect()

        conn.execute("""
            INSERT INTO assignments(

                ticket_id,
                ticket_number,
                ticket_title,

                customer_id,
                customer_name,

                organization_id,
                organization_name,

                group_id,
                group_name,

                priority_id,
                priority_name,

                state_id,
                state_name,

                agent_id,
                agent_name

            )
            VALUES(

                ?, ?, ?,
                ?, ?,
                ?, ?,
                ?, ?,
                ?, ?,
                ?, ?,
                ?, ?

            )
        """, (

            ticket["id"],
            ticket["number"],
            ticket["title"],

            ticket.get("customer_id"),
            ticket.get("customer_name", ""),

            ticket.get("organization_id"),
            ticket.get("organization_name", ""),

            ticket.get("group_id"),
            ticket.get("group_name", ""),

            ticket.get("priority_id"),
            ticket.get("priority_name", ""),

            ticket.get("state_id"),
            ticket.get("state_name", ""),

            agent["id"],
            f'{agent["firstname"]} {agent["lastname"]}'

        ))

        conn.commit()

        conn.close()

    ############################################################

    def total_assignments(self):

        conn = self.connect()

        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM assignments")

        total = c.fetchone()[0]

        conn.close()

        return total

    ############################################################

    def assignments_today(self):

        conn = self.connect()

        c = conn.cursor()

        c.execute("""
            SELECT
                agent_name,
                COUNT(*) total
            FROM assignments
            WHERE DATE(assigned_at)=DATE('now','localtime')
            GROUP BY agent_name
            ORDER BY total DESC
        """)

        rows = c.fetchall()

        conn.close()

        return rows

    ############################################################

    def last_assignments(self, limit=20):

        conn = self.connect()

        c = conn.cursor()

        c.execute("""
            SELECT
                ticket_number,
                customer_name,
                ticket_title,
                group_name,
                priority_name,
                state_name,
                agent_name,
                assigned_at
            FROM assignments
            ORDER BY assigned_at DESC
            LIMIT ?
        """, (limit,))

        rows = c.fetchall()

        conn.close()

        return rows
