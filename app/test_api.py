from zammad import ZammadAPI

api = ZammadAPI()

print()

print("==========")

print("Agentes:", len(api.agents_from_group()))

print("Tickets:", len(api.tickets()))

print("Abertos:", len(api.open_tickets()))

print("Recebidos Hoje:", len(api.received_today()))
