import utils
import getter
import processor
import click


@click.group()
def cli():
    pass


@cli.command(help="Downloads NS nations dump")
def download():
    config = utils.get_config()
    getter.get_dump(config)


@cli.command(help="Processes a downloaded dump")
def process():
    config = utils.get_config()
    processor.process_dump(config)


@cli.command(help="Processes endorsements from dump")
def endos():
    config = utils.get_config()
    processor.process_endos(config)


if __name__ == '__main__':
    cli()
