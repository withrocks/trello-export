#!/usr/bin/env python
import json
import yaml


class TrelloExport:
    def __init__(self, export_file_path, mapping_file_path, user_msg):
        user_msg("Loading export file from Trello from '{}'...".format(export_file_path))
        with open(export_file_path) as f:
            self.data = json.load(f)

        user_msg("Load mapping file from '{}'...".format(mapping_file_path))
        with open(mapping_file_path) as f:
            self.mapping = yaml.load(f)
            self.user_mapping = self.mapping['users']
            self.list_mapping = self.mapping['lists']

        self.members_indexed_by_id = {
            item['id']: item for item in self.data['members']}

        self.card_creators_indexed_by_card_id = {
            item['data']['card']['id']: item['idMemberCreator']
            for item in self.data['actions'] if item['type'] == 'createCard'}

        self.lists_indexed_by_id = {
            item['id']: item for item in self.data['lists']}

    def to_csv(self):
        """
        Maps the file to a CSV, without applying mapping

        The CSV includes all cards and all checklists
        """
        for card in self.data['cards']:
            yield {
                    'type': 'card',
                    'name': card['name'],
                    'desc': card['desc'],
                    'created_by': self.get_card_creator(card['id']),
                    'list_id': card['idList']
                  }

    def to_csv_mapped(self):
        # TODO: Apply mapping
        for entry in self.to_csv():
            yield {
                'type': entry['type'],
                'name': entry['name'],
                'desc': entry['desc'],
                'created_by': self.map_trello_user(entry['created_by']),
                'list': self.map_trello_list(entry['list_id'])
            }

    def map_trello_user(self, trello_user_id):
        field = self.mapping['users_mapping_from_field']
        key = self.members_indexed_by_id[trello_user_id][field]
        return self.user_mapping.get(key, key)

    def map_trello_list(self, trello_list_id):
        field = self.mapping['lists_mapping_from_field']
        key = self.lists_indexed_by_id[trello_list_id][field]
        return self.list_mapping.get(key, key)

    def get_card_creator(self, card_id):
        return self.card_creators_indexed_by_card_id[card_id]

    def get_list_name(self, list_id):
        return self.lists_indexed_by_id[list_id]['name']


"""
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
"""
