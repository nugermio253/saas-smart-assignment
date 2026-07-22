import sqlite3

DB = "state/round_robin.db"


class Statistics:

    def connect(self):
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        return conn

    def total_assignments(self):

        conn = self.connect()
        c = conn.cursor()

        c.execute("""
            SELECT COUNT(*)
            FROM assignments
        """)

        total = c.fetchone()[0]
        conn.close()

        return total

    def assignments_today(self):

        conn = self.connect()
        c = conn.cursor()

        c.execute("""
            SELECT COUNT(*)
            FROM assignments
            WHERE date(assigned_at)=date('now')
        """)

        total = c.fetchone()[0]
        conn.close()

        return total

    def last_assignments(self, limit=10):

        conn = self.connect()
        c = conn.cursor()

        c.execute("""
            SELECT
                ticket_id,
                agent_id,
                assigned_at
            FROM assignments
            ORDER BY assigned_at DESC
            LIMIT ?
        """, (limit,))

        rows = c.fetchall()
        conn.close()

        return rows

    def tickets_per_agent(self, api):

        users = api.users()

        nomes = {}

        for u in users:
            nomes[u["id"]] = f'{u["firstname"]} {u["lastname"]}'

        conn = self.connect()
        c = conn.cursor()

        c.execute("""
            SELECT
                agent_id,
                COUNT(*) total
            FROM assignments
            GROUP BY agent_id
            ORDER BY total DESC
        """)

        resultado = []

        for row in c.fetchall():

            resultado.append({
                "agent_id": row["agent_id"],
                "agent_name": nomes.get(
                    row["agent_id"],
                    f"ID {row['agent_id']}"
                ),
                "total": row["total"]
            })

        conn.close()

        return resultado
