import requests
import techs
import config

headers = {
    "Authorization": "Bearer " + config.TOKEN,
    "Content-Type": "application/json"
}
#CHECKING FOR AVAILABLE NEW TICKET
def get_new_tickets():

    url = config.BASE_URL + "/tickets/search"

    response = requests.get(url, headers=headers)

    return response.json()
#CHECKING TECH WORKLOAD TO ASSIGN TICKET
def get_tech_workload():

    workload = {}

    for name, tech_id in techs.techs.items():

        url = config.BASE_URL + "/tickets/search?ResponsibleUID=" + str(tech_id)

        response = requests.get(url, headers=headers)

        tickets = response.json()

        workload[name] = len(tickets)

    return workload
# ASSINGING TICKET TO THE TECH WITH THE FEWEST TICKET COUNTS
def get_available_tech():

    workload = get_tech_workload()

    return min(workload, key=workload.get)

def assign_ticket(ticket_id, tech_name):

    tech_id = techs.techs[tech_name]

    url = config.BASE_URL + "/tickets/" + str(ticket_id)

    data = {"ResponsibleUID": tech_id}

    requests.post(url, json=data, headers=headers)

    print("Ticket", ticket_id, "assigned to", tech_name)

def router():

    tickets = get_new_tickets()

    for ticket in tickets:

        tech = get_available_tech()

        assign_ticket(ticket["ID"], tech)

router()