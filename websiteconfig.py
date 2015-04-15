import os

_basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'tabs.db')

SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')

del os
