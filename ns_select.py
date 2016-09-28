# __author__ = lau
# 2016.9.27
import sqlite3
import init_db
import random


class NsSelector(init_db.DbInitiator):

    def __init__(self, db_path, f_path):
        init_db.DbInitiator.__init__(self, db_path, f_path)

    def _server_load_(self):
        if not self.__is_init__:
            self._db_init_(self.__f_path__)
        conn = sqlite3.connect(self.__db_path__)
        cursor = conn.cursor()
        locations = {}
        try:
            cursor.execute("SELECT LOCATION, NUM FROM LOCATIONS")
            for row in cursor:
                locations[row[0]] = row[1]
            print "[#]", len(locations), "locations exists, and", \
                reduce((lambda a, b: a + b), [locations[x] for x in locations]), "servers."
        except sqlite3.OperationalError, sqlite3.ProgrammingError:
            print "[!] Error:", Exception

        if len(locations) != 0:
            for x in locations:
                locations[x] = []
                try:
                    cursor.execute("SELECT IP FROM SERVERS WHERE fk_LOCATION IS ?", (x,))
                    for row in cursor:
                        locations[x].append(row[0].encode('utf8'))
                except sqlite3.OperationalError, sqlite3.ProgrammingError:
                    print Exception
            print '[#] Servers info loaded.'
        cursor.close()
        conn.close()
        return locations

    def select(self):
        server_list = []
        server_collection = self._server_load_()
        for location in server_collection:
            if len(server_collection[location]) > 1:
                server_list.append((location, server_collection[location][random.randint(0, len(server_collection
                                                                                                [location])) - 1]))
            else:
                server_list.append((location, server_collection[location][0]))
        return server_list
