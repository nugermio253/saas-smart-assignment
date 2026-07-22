from database import RoundRobinDB


class DashboardStatistics:

    def __init__(self):

        self.db = RoundRobinDB()

    ##########################################################

    def cards(self):

        return {
            "total_assignments": self.db.total_assignments(),
            "ranking": self.db.assignments_today()
        }

    ##########################################################

    def latest(self):

        return self.db.last_assignments(20)

    ##########################################################

    def chart_agents(self):

        conn = self.db.connect()

        c = conn.cursor()

        c.execute("""
            SELECT
                agent_name,
                COUNT(*) total
            FROM assignments
            GROUP BY agent_name
            ORDER BY total DESC
        """)

        data = []

        for row in c.fetchall():

            data.append({
                "agent": row["agent_name"],
                "tickets": row["total"]
            })

        conn.close()

        return data

    ##########################################################

    def chart_groups(self):

        conn = self.db.connect()

        c = conn.cursor()

        c.execute("""
            SELECT
                group_name,
                COUNT(*) total
            FROM assignments
            GROUP BY group_name
            ORDER BY total DESC
        """)

        data = []

        for row in c.fetchall():

            data.append({
                "group": row["group_name"],
                "tickets": row["total"]
            })

        conn.close()

        return data

    ##########################################################

    def chart_priorities(self):

        conn = self.db.connect()

        c = conn.cursor()

        c.execute("""
            SELECT
                priority_name,
                COUNT(*) total
            FROM assignments
            GROUP BY priority_name
            ORDER BY total DESC
        """)

        data = []

        for row in c.fetchall():

            data.append({
                "priority": row["priority_name"],
                "tickets": row["total"]
            })

        conn.close()

        return data

    ##########################################################

    def chart_hours(self):

        conn = self.db.connect()

        c = conn.cursor()

        c.execute("""
            SELECT
                strftime('%H', assigned_at) hour,
                COUNT(*) total
            FROM assignments
            GROUP BY hour
            ORDER BY hour
        """)

        data = []

        for row in c.fetchall():

            data.append({
                "hour": row["hour"],
                "tickets": row["total"]
            })

        conn.close()

        return data

    ##########################################################

    def chart_days(self):

        conn = self.db.connect()

        c = conn.cursor()

        c.execute("""
            SELECT
                date(assigned_at) day,
                COUNT(*) total
            FROM assignments
            GROUP BY day
            ORDER BY day
        """)

        data = []

        for row in c.fetchall():

            data.append({
                "day": row["day"],
                "tickets": row["total"]
            })

        conn.close()

        return data
