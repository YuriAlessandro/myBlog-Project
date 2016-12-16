import pymongo

from pyramid.config import Configurator
from urlparse import urlparse
from pymongo import MongoClient
from pyramid.events import NewRequest

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')

    db_url = urlparse(settings['mongo_uri'])

    config.registry.db = MongoClient(host=db_url.hostname, port=db_url.port,)
    conn = config.registry.db
    config.registry.settings['mongodb_conn'] = conn
    # config.registry.settings['logindb_conn'] = logindb_conn

    def add_db(request):
        db = config.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        return db

    config.add_request_method(add_db, 'db', reify=True)
    config.add_subscriber(add_mongo_db, NewRequest)
    config.include('project.routes')
    config.scan()
    return config.make_wsgi_app()

def _db(request):
    settings = request.registry.settings
    db_name = settings['mongodb.db_name']
    return settings['mongodb_conn'][db_name]

# def _logindb(request):
#     settings = request.registry.settings
#     db_name = settings['logindb.db_name']
#     return settings['logindb_conn'][db_name]

def add_mongo_db(event):
    # event.request.set_property(_logindb, 'logindb', reify=True)
    event.request.set_property(_db, 'db', reify=True)
