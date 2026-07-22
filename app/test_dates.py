from zammad import ZammadAPI

api = ZammadAPI()

tickets = api.received_today()

for t in tickets[:20]:
    print(
        t["id"],
        t["created_at"],
        t["title"]
    )

print("Total:", len(tickets))
