
from .DBManager import DBManager
from boto3.dynamodb.conditions import Key, Attr   
import logging
logger = logging.getLogger(__name__)

class BaseDataClass(object):
    """BaseDataClass that provides basic data class funtionalities"""

    # def __getattr__(self, key):
    #     if key in super(BaseDataClass, self).__getattr__('_attrMap'):
    #         return super(BaseDataClass, self).__getattr__('_attrMap')[key]
    #     else:
    #         return super(BaseDataClass, self).__getattr__(key)

    # def __setattr__(self, key, val):
    #     if key in self._attrMap:
    #         self._attrMap[key] = val
    #     else:
    #         super(BaseDataClass, self).__setattr__(key, value)

    def __init__(self, field_list, jsonObj=None):
        super(BaseDataClass, self).__init__()
        self._keys = field_list[0]
        self._field_list = field_list[1:] + field_list[0]
        for field in self._field_list:
            setattr(self, field, None)

        if jsonObj is not None:
            for key, val in jsonObj.items():
                if key in self._field_list:
                    setattr(self, key, jsonObj[key])

    def getAttrs(self):
        return self._field_list

    def getAttrMap(self):
        attrMap =  {}
        for field in self._field_list:
            attrMap[field] =  getattr(self, field)
        return attrMap

    def getKeys(self):
        return self._keys

    def getKeyDict(self):
        keyDict = {}
        for key in self.getKeys():
            keyVal = getattr(self, key)
            if keyVal is not None:
                keyDict[key] = keyVal
        return keyDict

    def __repr__(self):
        return str(self.getAttrMap())

    def __eq__(self, obj):
        return self.getAttrMap() == obj.getAttrMap()

    @classmethod
    def getItemTable(cls, item):
        className = item.__class__.__name__
        logger.info("Getting table: {}".format(className))
        return DBManager.table(className)

    @classmethod
    def addItem(cls, item, idGen=None):
        '''
            Use idGen to control the way id is generated
        '''
        itemTable = cls.getItemTable(item)
        keys = item.getKeys()
        logger.info("Keys are: {}".format(keys))
        def generateKeyConditionExpression(indexKeys, item):
            expression = Key(indexKeys[0]).eq(getattr(item, indexKeys[0]))
            if len(indexKeys) == 2:
                expression &= Key(indexKeys[1]).gt(0)
            return expression

        newId = 1
        if idGen is None:
            response = itemTable.query(
                Limit = 1,
                ScanIndexForward = False,
                KeyConditionExpression=generateKeyConditionExpression(keys, item)
            )
            if len(response['Items']):
                largestId = response['Items'][0][keys[1]]
                newId = int(largestId) + 1
        else:
            newId = idGen()
        # TODO: base on the input to decide what to add
        logger.info("Allocated id is :{}".format(newId))
        if len(keys) == 2:
            setattr( item, keys[1], newId)
        else:
            setattr( item, keys[0], newId)

        itemTable.put_item(
            Item=item.getAttrMap()
        )
        logger.info("Added item: {} to database".format(newId))
        
        return newId

    @classmethod
    def deleteItem(cls, item):
        '''
            only required element for item are key fields,
            returns true when deletion succed 
        '''
        itemTable = cls.getItemTable(item)
        try:
            itemTable.delete_item(
                Key= item.getKeyDict()
            )
        except Exception as e:
            logger.exception("Failed to delete item : {}".format(keyDict))
            return False
        else:
            logger.debug("Deleted item : {}".format(keyDict))
            return True

    @classmethod
    def updateItem(cls, item):
        itemTable = cls.getItemTable(item)
        exp = "set "
        valMap = {}
        for key in (set(item.getAttrs()) - set(item.getKeys())):
            attrVal = getattr(item, key)
            if attrVal:
                exp += " {keyName} = :{keyName},".format(keyName=key)
                valMap[":{}".format(key)] = DBManager.dataToStr(attrVal)
        try:
            resp = itemTable.update_item(
                Key= item.getKeyDict(),
                UpdateExpression = exp[:-1],
                ExpressionAttributeValues = valMap,
                ReturnValues="UPDATED_NEW"
            )
        except Exception as e:
            logger.exception("Failed to update item: {}".format(item.getKeyDict()))
            return False
        else:
            return True

    @classmethod
    def getItem(cls, item):
        '''
            only required element for item are key fields
        '''
        keys = item.getKeyDict()
        itemTable = cls.getItemTable(item)

        logger.info("Getting item: {}".format(keys))
        response = itemTable.get_item(
            Key= keys
        )

        reItem = DBManager.toJsonData(response['Item'])
        logger.debug("Returning item: {}".format(keys))
        return reItem

    @classmethod
    def getItems(cls, item):
        pass