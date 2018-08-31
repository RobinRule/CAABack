from .setupDynamoDB         import getDynamoDBConnection, createCasesTable
from uuid                   import uuid4

class ConnectionManager:

    def __init__(self, mode=None, config=None, endpoint=None, port=None, use_instance_metadata=False):
        self.db = None
        self.tables = {}
        if mode == "local":
            if config is not None:
                raise Exception('Cannot specify config when in local mode')
            if endpoint is None:
                endpoint = 'localhost'
            if port is None:
                port = 8000
            self.db = getDynamoDBConnection(endpoint=endpoint, port=port, local=True)
        elif mode == "service":
            self.db = getDynamoDBConnection(config=config, endpoint=endpoint, use_instance_metadata=use_instance_metadata)
        else:
            raise Exception("Invalid arguments, please refer to usage.");

        self.setupTable('Cases')

    def setupTable(self, tableName):
        try:
            self.tables[tableName] = self.db.Table(tableName)
        except Exception as e:
            logger.exception("There was an issue trying to retrieve the {} table.".format(tableName))
            self.createTable(tableName)

    def getTable(self, tableName):
        if self.tables.get(tableName) is None:
            self.setupTable(tableName)
        return self.tables[tableName]

    def createTable(self, tableName):
        if tableName == 'Cases':
            self.tables[tableName] = createCasesTable(self.db)
