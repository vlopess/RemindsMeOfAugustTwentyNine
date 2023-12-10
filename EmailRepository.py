import os
import sys
from EmailException import EmailException


curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.append(os.path.split(rootPath)[0])



from connection import DBConnectionHandler


class emailRepository:
    def selectwhere(self, email):
        with DBConnectionHandler() as db:
            try:
                cur = db.getCursor()
                cur.execute("SELECT * FROM EMAIL WHERE email = %s;", (email,))
                results = cur.fetchall()
                if len(results) != 0:
                    raise EmailException
            except Exception as exception:
                raise exception
    def select(self):
        with DBConnectionHandler() as db:
            try:
                cur = db.getCursor()
                cur.execute("SELECT * FROM EMAIL;")
                results = cur.fetchall()
                map = {}
                for result in results:
                        map[result[0]] = result[1]
                return map
            except Exception as exception:
                raise exception
    def insert(self, email):
        with DBConnectionHandler() as db:
            try:
                cur = db.getCursor()
                cur.execute("INSERT INTO EMAIL (EMAIL) VALUES (%s)", (email,))
                db.commitar()
            except Exception as exception:
                raise exception
