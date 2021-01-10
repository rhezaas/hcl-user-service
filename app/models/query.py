from sqlalchemy import insert, update, delete


class QueryModel:
    def __init__(self, transaction):
        self.__transaction__ = transaction
        self.__insert__ = None
        self.__update__ = None
        self.__delete__ = None

    def select(self, table):
        return self.__transaction__.query(table)

    def insert(self, table):
        self.__insert__ = insert(table)
        return self

    def update(self, table):
        self.__update__ = update(table)
        return self

    def delete(self, table):
        self.__delete__ = delete(table)
        return self

    def where(self, clause):
        if not (self.__update__ is None):
            self.__update__ = self.__update__.where(clause)
        elif not (self.__delete__ is None):
            self.__delete__ = self.__delete__.where(clause)
        return self

    def values(self, *args, **kwargs):
        if not (self.__insert__ is None):
            self.__insert__ = self.__insert__.values(*args, **kwargs)
        elif not (self.__update__ is None):
            self.__update__ = self.__update__.values(*args, **kwargs)
        return self

    def returning(self, *cols):
        if not (self.__insert__ is None):
            self.__insert__ = self.__insert__.returning(*cols)
        elif not (self.__update__ is None):
            self.__update__ = self.__update__.returning(*cols)
        return self

    def execute(self):
        if not (self.__insert__ is None):
            result = self.__insert__
            self.__insert__ = None
        elif not (self.__update__ is None):
            result = self.__update__
            self.__update__ = None
        elif not (self.__delete__ is None):
            result = self.__delete__
            self.__delete__ = None

        return self.__transaction__.execute(result)
