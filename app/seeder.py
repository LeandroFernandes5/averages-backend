import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,  create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

dbURI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://averages:averages@localhost:6543/flask'

Base = declarative_base()
DBSession = scoped_session(sessionmaker())
engine = None


def init_sqlalchemy(dbname=dbURI):
    global engine
    engine = create_engine(dbname, echo=False)
    DBSession.remove()
    DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)

def truncate_tables():
    engine = create_engine(dbURI, echo = True)
    conn = engine.connect()
    tables = engine.table_names()

    for table in tables:
        if table == 'alembic_version':
            pass
        else:
            conn.engine.execute('TRUNCATE TABLE ' + table + ' RESTART IDENTITY CASCADE')


def load_user():
    init_sqlalchemy()
    # user = User(
    #     email = 'leandrojlfernandes@gmail.com',
    #     name = 'Leandro Fernandes'
    # )
    # user.set_password('esLarilas')

    DBSession.commit()
    print('Passei na funcao')



if __name__ == '__main__':
    truncate_tables()
    load_user()

