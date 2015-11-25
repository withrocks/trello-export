def map_to_jira_ticket(trello_ticket):
    return {'IssueType': 'Story' if trello_ticket['type'] == 'card' else 'Sub-task',
            'Summary': trello_ticket['name'],
            'Description': trello_ticket['desc'],
            'Reporter': trello_ticket['created_by'],
            'Status': trello_ticket['list'],
            'Issue ID': trello_ticket['export_id'],
            'Parent ID': trello_ticket['parent_export_id']}


# https://confluence.atlassian.com/jira/importing-data-from-csv-185729516.html
def format_output_column(column):
    if not column:
        return u''
    elif type(column) == unicode or type(column) == str:
        # Escape quotes:
        column = column.replace('"', '""')
    return u'"{}"'.format(column)

