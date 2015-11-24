import click
from trello_export.main import TrelloExport


@click.group()
@click.option('--config')
@click.pass_context
def cli(ctx, config):
    pass


@cli.command('to-csv')
@click.argument('export')
@click.argument('mapping')
@click.pass_context
def to_csv(ctx, export, mapping):
    """
    Export the json to a CSV file that can be used to import
    into JIRA for example.
    """
    def notify(msg):
        print msg
    trello = TrelloExport(export, mapping, notify)

    for line in trello.to_csv_mapped():
        print line



def main():
    cli(obj={})

if __name__ == "__main__":
    main()

