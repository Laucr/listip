# __author__ = lau
# 2016.9.26
import sqlite3


class DbInitiator:

    __version__ = '1.0'
    __author__ = 'Lau'
    __is_init__ = False

    def __init__(self, db_path, f_path):
        self.__db_path__ = db_path
        self.__f_path__ = f_path

    @staticmethod
    def server_info(path='servers.txt'):

        server_location = {}
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                item = line.split()
                if len(item) == 2:
                    if item[0] not in server_location:
                        server_location[item[0]] = [item[1]]
                    else:
                        server_location[item[0]].append(item[1])
        return server_location

    def _db_init_(self, f_path):
        conn = sqlite3.connect(self.__db_path__)
        conn.text_factory = str
        record_count = 0
        try:
            cursor = conn.execute('SELECT COUNT(*) FROM SERVERS')
            for row in cursor:
                record_count = row[0]
            print '[*] Database', self.__db_path__, 'loaded successfully.'
            cursor.close()
        except sqlite3.OperationalError:
            conn.execute("CREATE TABLE LOCATIONS (LOCATION CHAR(20) PRIMARY KEY NOT NULL, NUM INTEGER NOT NULL) ")
            conn.execute("CREATE TABLE SERVERS (IP CHAR(16) PRIMARY KEY NOT NULL,\
                          fk_LOCATION CHAR(20) REFERENCES LOCATIONS(LOCATION));")
        server_location = self.server_info(self.__f_path__)
        if record_count == 0:
            cursor = conn.cursor()
            for location in server_location:
                cursor.execute("INSERT INTO LOCATIONS (LOCATION, NUM) \
                                VALUES (?,?)", (location, len(server_location[location])))
                for ip in server_location[location]:
                    cursor.execute("INSERT INTO SERVERS (IP, fk_LOCATION)\
                                    VALUES (?,?);", (ip, location))
            conn.commit()
            print '[*] Servers info created successfully.'
            cursor.close()
        else:
            print '[*]', record_count, 'record(s) exists.'
        self.__is_init__ = True
