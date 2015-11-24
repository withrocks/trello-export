#!/usr/bin/env python

import json
import yaml

from jira_csv import CsvGenerator, CsvEntry

print "Loading export file from Trello, at export.json..."
with open("export.json") as f:
    data = json.load(f)


# Get the trello lists, indexed by the list id
trello_lists = {item["id"]: item for item in data["lists"]}
print "Trello lists {}".format(len(trello_lists))

print "Load mapping file..."
with open('mapping.yaml') as f:
    mapping = yaml.load(f)

# Ensure your mapping file has trello users (full names) mapped to jira usernames:
trello_user_to_jira = mapping['trello_user_to_jira']

# Now get a list of all members in trello, with mapping data:
print mapping

members = {member['id']: trello_user_to_jira[member['fullName']] for member in data["members"]}
print members

# Now, we're interested in the actions, since they show who created the cards,
# which we will map to Reported:
cards_created_by_user = {item['data']['card']['id']: members[item['idMemberCreator']]
                         for item in data['actions'] if item['type'] == 'createCard'}

# Now we got all "Reported by" in all cards
trello_list_to_jira_status = mapping['trello_list_to_jira_status']
print trello_list_to_jira_status

def get_jira_status_from_trello_list(list_id):
    if list_id in trello_list_to_jira_status:
        return trello_list_to_jira_status[list_id]


list_to_jira_status = {item['id']: get_jira_status_from_trello_list(item['name']) for item in data['lists']}
print list_to_jira_status



csv = CsvGenerator()
with open('report.csv', 'w') as outfile:
    outfile.truncate()
    for card in data["cards"]:
        if not card['closed']:
            #print u"name={},desc={},reported={}".format(
            #    card['name'], card['desc'], cards_created_by_user[card['id']])

            jira_status = get_jira_status_from_trello_list(card['idList'])
            # TODO: All stories for now, need to pick up bug labels
            entry = CsvEntry('story', list_to_jira_status[card['idList']], card['name'], card['desc'])

            outfile.write(entry.issue_type)
            outfile.write(u'\n')
