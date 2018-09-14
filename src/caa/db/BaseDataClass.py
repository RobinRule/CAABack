
from .DBManager import DBManager
from boto3.dynamodb.conditions import Key, Attr

class BaseDataClass(object):
    """BaseDataClass that provides basic data class funtionalities"""

    def __getattr__(self, key):
        return self._attrMap[key]

    def __setattr__(self, key, val):
        self._attrMap[key] = val

    def __init__(self, field_list, jsonObj=None):
        self._keys = field_list[0]
        self._field_list = field_list[1:] + field_list[0]
        self._attrMap = {}
        if jsonObj is not None:
            for key, val in jsonObj.iteritems():
                if key in self._field_list:
                    self._attrMap[key] = jsonObj[key]

    def getAttrs(self):
        return self._field_list

    def getAttrMap(self):
        return self._attrMap

    def getKeys(self):
        return self._keys

    def __repr__(self):
        return str(self._attrMap)

    def __eq__(self, obj):
        return self._attrMap == obj._attrMap

    @classmethod
    def addItem(cls, item):
        className = item.__class__.__name__
        itemTable = DBManager.table(className)

        keys = item.getKeys()
        def generateKeyConditionExpression(indexKeys, item):
            expression = Key(indexKeys[0]).eq(getattr(item, indexKeys[0]))
            if len(indexKeys) == 2:
                expression &= Key(indexKeys[1]).gt(0)
            return expression


        response = itemTable.query(
            Limit = 1,
            ScanIndexForward = False,
            KeyConditionExpression=generateKeyConditionExpression(keys, item)
        )
        newId = 1
        if len(response['Items']):
            largestId = response['Items'][0][keys[1]]
            newId = int(largestId) + 1

        # TODO: base on the input to decide what to add
        logger.info("Allocated id is :{}".format(newId))
        itemTable.put_item(
            Item=item.getAttrMap()
        )
        logger.info("Added item: {} to database".format(newId))
        
        return newId

    @classmethod
    def deleteItem(cls, keys):
        pass

    @classmethod
    def updateItem(cls, item):
        pass

    @classmethod
    def getItem(cls, keys):
        pass

    @classmethod
    def getItems(cls, ):
        pass