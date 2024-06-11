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


@cli.command(help="Download and process dump")
def update():
    config = utils.get_config()
    if getter.get_dump(config):
        processor.process_dump(config)


if __name__ == '__main__':
    cli()
