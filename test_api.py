from zammad import ZammadAPI

api = ZammadAPI()

print("Recebidos:", len(api.received_today()))
print("Abertos:", len(api.open_tickets()))
print("Fechados:", len(api.closed_today()))
