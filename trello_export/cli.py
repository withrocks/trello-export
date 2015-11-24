import click
from trello_export.main import TrelloExport
from jira_csv import map_to_jira_ticket


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command('to-jira-csv')
@click.argument('export')
@click.argument('mapping')
@click.pass_context
def to_jira_csv(ctx, export, mapping):
    """
    Export the json to a CSV file that can be used to import
    into JIRA for example.
    """
    def notify(msg):
        print msg
    trello = TrelloExport(export, mapping, notify)

    # TODO: All issues are currently stories, mark as Bug
    # if they have the label bug
    print "IssueType,Summary,Description,Reporter,Status, Issue ID, Parent ID"
    for ticket in trello.to_csv_mapped():
        jira_ticket = map_to_jira_ticket(ticket)
        line = [jira_ticket['IssueType'],
                jira_ticket['Summary'],
                jira_ticket['Description'],
                jira_ticket['Reporter'],
                jira_ticket['Status'],
                jira_ticket['Issue ID'],
                jira_ticket['Parent ID']]
        line = map(unicode, line)
        print u",".join(line)




def main():
    cli(obj={})

if __name__ == "__main__":
    main()

