from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config


class Database:
    Base = declarative_base()
    Engine = create_engine('postgresql+psycopg2://%s:%s@%s:%s/%s' % (
        config('DB_USER'),
        config('DB_PASS'),
        config('DB_HOST'),
        config('DB_PORT'),
        config('DB_NAME')
    ), echo=True if config('DB_DEBUG') == 'true' else False,
        pool_pre_ping=True,
        pool_size=1
    )
    Session = sessionmaker(bind=Engine, autocommit=False)
    Transaction = Session()

    # transaction
    def transaction(self):
        return self.Transaction

    def close(self):
        return self.Engine.dispose()

    def commit(self):
        return self.Transaction.commit()

    def flush(self):
        return self.Transaction.flush()

    def rollback(self):
        return self.Transaction.rollback()
