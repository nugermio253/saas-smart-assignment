import time
import yaml
import requests
from datetime import date


class ZammadAPI:

    def __init__(self):

        with open("config/config.yaml", "r") as f:
            cfg = yaml.safe_load(f)

        self.base = cfg["zammad"]["url"].rstrip("/")
        self.token = cfg["zammad"]["token"]

        self.exclude_users = cfg["assignment"].get(
            "exclude_users",
            []
        )

        self.headers = {
            "Authorization": f"Token token={self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Cache dos tickets
        self._tickets_cache = None
        self._tickets_cache_time = 0
        self.cache_timeout = 30

    ####################################################################
    # REQUEST
    ####################################################################

    def request(self, endpoint, params=None):

        url = f"{self.base}{endpoint}"

        r = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30
        )

        print(f"GET {r.url}")
        print(f"HTTP {r.status_code}")

        if not r.ok:
            print(r.text)
            return None

        return r.json()

    ####################################################################
    # USERS
    ####################################################################

    def me(self):

        return self.request("/api/v1/users/me")

    def users(self):

        return self.request("/api/v1/users")

    ####################################################################
    # GROUPS
    ####################################################################

    def groups(self):

        return self.request("/api/v1/groups")

    ####################################################################
    # TICKET
    ####################################################################

    def ticket(self, ticket_id):

        return self.request(
            f"/api/v1/tickets/{ticket_id}"
        )

    ####################################################################
    # TODOS OS TICKETS (COM CACHE)
    ####################################################################

    def tickets(self):

        # usa cache
        if (
            self._tickets_cache is not None
            and
            (time.time() - self._tickets_cache_time)
            < self.cache_timeout
        ):

            print("Usando cache dos tickets")

            return self._tickets_cache

        tickets = []

        page = 1

        while True:

            data = self.request(
                "/api/v1/tickets",
                params={
                    "page": page,
                    "per_page": 100
                }
            )

            if not data:
                break

            tickets.extend(data)

            print(
                f"Página {page}: {len(data)} tickets"
            )

            if len(data) < 100:
                break

            page += 1

        self._tickets_cache = tickets
        self._tickets_cache_time = time.time()

        return tickets

    ####################################################################
    # TICKETS SEM OWNER
    ####################################################################

    def unassigned_tickets(self):

        return self.request(
            "/api/v1/tickets/search",
            params={
                "query": "owner_id:1"
            }
        )

    ####################################################################
    # ATRIBUIR
    ####################################################################

    def update_ticket_owner(
        self,
        ticket_id,
        owner_id
    ):

        url = f"{self.base}/api/v1/tickets/{ticket_id}"

        r = requests.put(
            url,
            headers=self.headers,
            json={
                "owner_id": owner_id
            },
            timeout=30
        )

        print(f"PUT {url}")
        print(f"HTTP {r.status_code}")

        if not r.ok:
            print(r.text)
            return False

        return True

    def assign(self, ticket_id, owner):

        return self.update_ticket_owner(
            ticket_id,
            owner
        )

    ####################################################################
    # AGENTES
    ####################################################################

    def agents_from_group(
        self,
        group_id=1
    ):

        users = self.users()

        agents = []

        for user in users:

            if not user.get("active"):
                continue

            if user.get("login") == "zammad@saasmaputo.co.mz":
                continue

            if user["id"] in self.exclude_users:
                continue

            groups = user.get(
                "group_ids",
                {}
            )

            if str(group_id) not in groups:
                continue

            if "full" not in groups[str(group_id)]:
                continue

            agents.append(user)

        return agents

    ####################################################################
    # ESTATÍSTICAS
    ####################################################################

    def open_tickets(self):

        tickets = self.tickets()

        return [
            t for t in tickets
            if t["state_id"] in [1, 2, 3]
        ]

    def closed_tickets(self):

        tickets = self.tickets()

        return [
            t for t in tickets
            if t["state_id"] == 4
        ]

    def received_today(self):

        hoje = str(date.today())

        tickets = self.tickets()

        resultado = []

        for ticket in tickets:

            if ticket["created_at"][:10] == hoje:
                resultado.append(ticket)

        return resultado

    ####################################################################
    # CACHE
    ####################################################################

    def clear_cache(self):

        self._tickets_cache = None
        self._tickets_cache_time = 0
