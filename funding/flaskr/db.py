import pymongo
from flask import current_app, g
import click
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = pymongo.MongoClient(current_app.config['MONGO_URI'])[current_app.config['MONGO_DB']]
    return g.db


def init_db():
    db = get_db()
    # TODO: initialize database if necessary


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    # app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)