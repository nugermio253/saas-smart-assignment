from flask import Blueprint, jsonify

from dashboard_statistics import DashboardStatistics
from zammad import ZammadAPI

api = ZammadAPI()
stats = DashboardStatistics()

dashboard_api = Blueprint(
    "dashboard_api",
    __name__
)


###########################################################
# Cards
###########################################################

@dashboard_api.route("/api/dashboard/cards")
def cards():

    agents = api.agents_from_group(1)
    pending = api.unassigned_tickets()

    return jsonify({

        "agents": len(agents),

        "pending": len(pending),

        "total_assignments": stats.db.total_assignments(),

        "today": stats.db.assignments_today()

    })


###########################################################
# Ranking
###########################################################

@dashboard_api.route("/api/dashboard/ranking")
def ranking():

    return jsonify(
        stats.chart_agents()
    )


###########################################################
# Últimas atribuições
###########################################################

@dashboard_api.route("/api/dashboard/latest")
def latest():

    data = []

    for row in stats.latest():

        data.append(dict(row))

    return jsonify(data)


###########################################################
# Tickets por agente
###########################################################

@dashboard_api.route("/api/dashboard/chart/agents")
def chart_agents():

    return jsonify(
        stats.chart_agents()
    )


###########################################################
# Tickets por grupo
###########################################################

@dashboard_api.route("/api/dashboard/chart/groups")
def chart_groups():

    return jsonify(
        stats.chart_groups()
    )


###########################################################
# Tickets por prioridade
###########################################################

@dashboard_api.route("/api/dashboard/chart/priorities")
def chart_priorities():

    return jsonify(
        stats.chart_priorities()
    )


###########################################################
# Tickets por hora
###########################################################

@dashboard_api.route("/api/dashboard/chart/hours")
def chart_hours():

    return jsonify(
        stats.chart_hours()
    )


###########################################################
# Tickets por dia
###########################################################

@dashboard_api.route("/api/dashboard/chart/days")
def chart_days():

    return jsonify(
        stats.chart_days()
    )
