import logging

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class SQLAlchemy:
    def __init__(self, app: FastAPI = None, **kwargs):
        self.__engine = None
        self.__session = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI, **kwargs):

        """
        DB Initial function
        param app:FastAPI
        param kwargs
        """

        database_url = kwargs.get("DB_URL")

        self.__engine = create_engine(database_url, echo=True, pool_pre_ping=True)

        self.__session = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)

        @app.on_event("startup")
        def start_up():
            self.__engine.connect()
            logging.info("DB Connected!")

        @app.on_event("shutdown")
        def shutdown():
            self.__session.close_all()
            self.__engine.dispose()
            logging.info("DB Disconnected!")

    def get_db(self):

        """
        Session persistence function
        """

        if self.__session is None:
            raise Exception("must be called 'init_app' first.")
        db_session = None
        try:
            db_session = self.__session()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self.__engine


db = SQLAlchemy()
Base = declarative_base()
