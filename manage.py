#!/usr/bin/env python
import os

from thermos import create_app, db
from thermos.models import User, Bookmark, Tag
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('THERMOS_ENV') or 'dev')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def insert_data():
    mickey = User(username="mickey", email="mickey@mouse.com", password="test")
    db.session.add(mickey)

    minnie = User(username="minnie", email="minnie@mouse.com", password="test")
    db.session.add(minnie)

    tag1 = Tag(name="news")
    db.session.add(tag1)

    tag2 = Tag(name="music")
    db.session.add(tag2)

    db.session.add(Bookmark(url="https://www.cnn.com", description="cnn", user=mickey, tags="news"))
    db.session.add(Bookmark(url="https://www.mtv.com", description="mtv", user=minnie, tags="music, news"))

    db.session.commit()

    print('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print('Dropped the database')


if __name__ == '__main__':
    manager.run()
