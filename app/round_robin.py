from database import RoundRobinDB


class RoundRobin:

    def __init__(self, agents):

        self.db = RoundRobinDB()

        self.agents = sorted(agents)

    ############################################################
    # Próximo agente
    ############################################################

    def next(self):

        if len(self.agents) == 0:
            return None

        last = self.db.get_last_agent()

        if last not in self.agents:

            agent = self.agents[0]

            self.db.save_last_agent(agent)

            return agent

        index = self.agents.index(last) + 1

        if index >= len(self.agents):
            index = 0

        agent = self.agents[index]

        self.db.save_last_agent(agent)

        return agent

    ############################################################
    # Ticket atribuído
    ############################################################

    def assigned(self, ticket_id, agent_id):

        # Neste momento apenas mantemos o método
        # para compatibilidade. O histórico é gravado
        # diretamente pelo main.py.
        return True
