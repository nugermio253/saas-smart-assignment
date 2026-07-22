import time


class ZammadCache:

    def __init__(self, api):

        self.api = api

        self.timeout = 300  # 5 minutos

        self.last_update = 0

        self.users = {}
        self.groups = {}
        self.organizations = {}
        self.priorities = {}
        self.states = {}

    def refresh(self):

        now = time.time()

        if (now - self.last_update) < self.timeout:
            return

        print("Atualizando cache do Zammad...")

        #
        # USERS
        #
        self.users = {}

        for u in self.api.users():

            self.users[u["id"]] = u

        #
        # GROUPS
        #
        self.groups = {}

        groups = self.api.request("/api/v1/groups")

        for g in groups:

            self.groups[g["id"]] = g

        #
        # ORGANIZATIONS
        #
        self.organizations = {}

        orgs = self.api.request("/api/v1/organizations")

        for o in orgs:

            self.organizations[o["id"]] = o

        #
        # PRIORITIES
        #
        self.priorities = {}

        priorities = self.api.request("/api/v1/ticket_priorities")

        for p in priorities:

            self.priorities[p["id"]] = p

        #
        # STATES
        #
        self.states = {}

        states = self.api.request("/api/v1/ticket_states")

        for s in states:

            self.states[s["id"]] = s

        self.last_update = now

    ###############################################################

    def enrich_ticket(self, ticket):

        self.refresh()

        #
        # Cliente
        #
        customer = self.users.get(
            ticket.get("customer_id")
        )

        if customer:

            ticket["customer_name"] = (
                customer["firstname"] +
                " " +
                customer["lastname"]
            )

        else:

            ticket["customer_name"] = ""

        #
        # Grupo
        #
        group = self.groups.get(
            ticket.get("group_id")
        )

        if group:

            ticket["group_name"] = group["name"]

        else:

            ticket["group_name"] = ""

        #
        # Organização
        #
        org = self.organizations.get(
            ticket.get("organization_id")
        )

        if org:

            ticket["organization_name"] = org["name"]

        else:

            ticket["organization_name"] = ""

        #
        # Prioridade
        #
        priority = self.priorities.get(
            ticket.get("priority_id")
        )

        if priority:

            ticket["priority_name"] = priority["name"]

        else:

            ticket["priority_name"] = ""

        #
        # Estado
        #
        state = self.states.get(
            ticket.get("state_id")
        )

        if state:

            ticket["state_name"] = state["name"]

        else:

            ticket["state_name"] = ""

        return ticket
