import jaydebeapi
import mysql.connector

class Datastore(object):

    def __init__(self, username, password, host, port, database):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def executeQuery(self, conn, sqlQuery):
        cursor = conn.cursor()
        cursor.execute(sqlQuery)
        return cursor.fetchall()


# child class
class MySql(Datastore):
    def __init__(self, username, password, host, port, database):
        Datastore.__init__(self, username, password, host, port, database)

    def getConnection(self):
        return mysql.connector.connect(
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )


class Dremio(Datastore):
    def __init__(self, username, password, host, port, database, jdbcDriverPath):
        self.jdbcDriverPath = jdbcDriverPath
        Datastore.__init__(self, username, password, host, port, database)

    def getConnection(self):
        return jaydebeapi.connect(
            "com.dremio.jdbc.Driver",
            "jdbc:dremio:direct={}:{};schema={}".format(self.host, self.port, self.database),
            [self.username, self.password],
            self.jdbcDriverPath
        )
