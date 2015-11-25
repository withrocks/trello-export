import click
from trello_export.main import TrelloExport
from jira_csv import map_to_jira_ticket, format_output_column


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command('to-jira-csv')
@click.argument('export')
@click.argument('mapping')
@click.option('--ignore', help='Comma separated list of Trello lists to ignore')
@click.option('--start', help='First sequence number for exported IDs (Issue Id)')
@click.pass_context
def to_jira_csv(ctx, export, mapping, ignore, start, encoding='utf-8'):
    """
    Export the json to a CSV file that can be used to import
    into JIRA for example.
    """
    trello = TrelloExport(export, mapping)

    ignore_list = ignore.split(',') if ignore else []
    start_id = int(start) if start else 1
    print "IssueType,Summary,Description,Reporter,Status, Issue Id, Parent Id"
    for ticket in filter(lambda current: current['list'] not in ignore_list,
                         trello.export_table_mapped(export_id_start=start_id)):
        jira_ticket = map_to_jira_ticket(ticket)
        line = [jira_ticket['IssueType'],
                jira_ticket['Summary'],
                jira_ticket['Description'],
                jira_ticket['Reporter'],
                jira_ticket['Status'],
                jira_ticket['Issue ID'],
                jira_ticket['Parent ID']]
        line = [format_output_column(column) for column in line]
        print u",".join(line).encode(encoding)


def main():
    cli(obj={})

if __name__ == "__main__":
    main()

