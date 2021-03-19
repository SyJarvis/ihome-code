# -*- coding:utf-8 -*-

from ihome import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# product develop

app = create_app('product')

manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()







