#!/usr/bin/env python
import json
import yaml
import copy


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
            self.labels_mapping = self.mapping['labels']

        self.members_indexed_by_id = {
            item['id']: item for item in self.data['members']}

        self.card_creators_indexed_by_card_id = {
            item['data']['card']['id']: item['idMemberCreator']
            for item in self.data['actions'] if item['type'] == 'createCard'}

        self.lists_indexed_by_id = {
            item['id']: item for item in self.data['lists']}

        self.checklists_indexed_by_id = {
            checklist['id']: checklist for checklist in self.data['checklists']}

    def to_csv(self, expand_checklists=True):
        """
        Maps the file to a CSV, without applying mapping

        The CSV includes all cards and all checklists
        """
        export_id = 0
        for card in self.data['cards']:
            export_id += 1
            ret = dict()
            ret['list_id'] = card['idList']
            ret['type'] = 'card'
            ret['created_by'] = self.get_card_creator(card['id'])
            ret['label'] = self.flatten_card_labels(card)
            ret['export_id'] = export_id
            ret['parent_export_id'] = None
            ret['name'] = card['name']
            ret['desc'] = card['desc']

            yield ret

            if expand_checklists:
                for checklist_item in self.enumerate_check_items(card, ret):
                    yield checklist_item

    def enumerate_check_items(self, card, card_exp):
        for checklist_id in card['idChecklists']:
            checklist = self.checklists_indexed_by_id[checklist_id]
            for item in checklist['checkItems']:
                yield {'type': 'check_item',
                       'name': item['name'],
                       'desc': '',
                       'created_by': card_exp['created_by'],
                       'export_id': None,
                       'parent_export_id': card_exp['export_id'],
                       'list_id': card_exp['list_id'],
                       'label': ''}

    def to_csv_mapped(self):
        # TODO: Export columns conditionally, such as if
        # label `a`, then column `x`=`b`
        for entry in self.to_csv():
            ret = copy.deepcopy(entry)
            ret['created_by'] = self.map_trello_user(entry['created_by'])
            ret['list'] = self.map_trello_list(entry['list_id'])
            ret['label'] = self.map_trello_label(entry['label'])
            yield ret

    def flatten_card_labels(self, card):
        return ",".join(item['name'] for item in card['labels'])

    def map_trello_user(self, trello_user_id):
        field = self.mapping['users_mapping_from_field']
        key = self.members_indexed_by_id[trello_user_id][field]
        return self.user_mapping.get(key, key)

    def map_trello_list(self, trello_list_id):
        field = self.mapping['lists_mapping_from_field']
        key = self.lists_indexed_by_id[trello_list_id][field]
        return self.list_mapping.get(key, key)

    def map_trello_label(self, trello_label):
        # TODO: Handle a list of labels
        return self.labels_mapping.get(trello_label, trello_label)

    def get_card_creator(self, card_id):
        return self.card_creators_indexed_by_card_id[card_id]

    def get_list_name(self, list_id):
        return self.lists_indexed_by_id[list_id]['name']

