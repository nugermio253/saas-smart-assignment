import time

from zammad import ZammadAPI
from cache import ZammadCache
from round_robin import RoundRobin
from database import RoundRobinDB

api = ZammadAPI()
cache = ZammadCache(api)
db = RoundRobinDB()

print("=" * 60)
print("SAAS SMART ASSIGNMENT")
print("=" * 60)

while True:

    # Agentes disponíveis
    agents = api.agents_from_group(1)

    print(f"\nAgentes disponíveis: {len(agents)}")

    if len(agents) == 0:
        print("Nenhum agente disponível.")
        time.sleep(10)
        continue

    # IDs para o Round Robin
    agent_ids = [a["id"] for a in agents]

    rr = RoundRobin(agent_ids)

    # Tickets sem proprietário
    tickets = api.unassigned_tickets()

    if tickets is None:
        print("Erro ao consultar tickets.")
        time.sleep(10)
        continue

    print(f"Tickets por atribuir: {len(tickets)}")

    if len(tickets) == 0:
        print("Nenhum ticket pendente.")
        time.sleep(10)
        continue

    for ticket in tickets:

        owner_id = rr.next()

        if owner_id is None:
            break

        # Procura o agente correspondente
        agent = next(
            (a for a in agents if a["id"] == owner_id),
            None
        )

        if agent is None:
            print(f"Agente {owner_id} não encontrado.")
            continue

        print(
            f"Atribuindo Ticket {ticket['number']} -> "
            f"{agent['firstname']} {agent['lastname']}"
        )

        # Atribui o ticket
        if api.assign(ticket["id"], owner_id):

            # Atualiza o Round Robin
            rr.assigned(ticket["id"], owner_id)

            # Enriquece o ticket com nomes
            ticket = cache.enrich_ticket(ticket)

            # Guarda na base de dados
            db.register_assignment(
                ticket,
                agent
            )

            print("OK")

        else:

            print("ERRO")

    print("\nNova verificação em 10 segundos...\n")

    time.sleep(10)
