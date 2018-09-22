
from .DBManager import DBManager
from boto3.dynamodb.conditions import Key, Attr
from global_var import Errors
import operator
from datetime import datetime
from dateutil.parser import parse as timeParse
from copy import deepcopy
import random
import string
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

    def __init__(self, fieldList, jsonObj=None):
        super(BaseDataClass, self).__init__()

        setattr(self, 'key', fieldList[0][0])

        self._fieldTypeMap = {}
        for fieldName, fieldType in fieldList:
            self._fieldTypeMap[fieldName] = fieldType

        for field in self._fieldTypeMap.keys():
            setattr(self, field, None)
        logger.info("Initializing using:{}".format(jsonObj))
        if jsonObj is not None:
            jsonObj = self.schemalize(jsonObj)
            for key, val in jsonObj.items():
                if key in self._fieldTypeMap and jsonObj[key] is not None:
                    setattr(self, key, jsonObj[key])

    def _convertDataToType(self, data, targetType):
        if targetType is datetime:
            return timeParse(data)
        else:
            return targetType(data)

    def schemalize(self, jsonObj):
        res = deepcopy(jsonObj)
        for key, val in jsonObj.items():
            if val is None:
                del res[key]
                continue

            resVal = val
            resType = self._fieldTypeMap[key]
            if type(val) is not resType:
                resVal = self._convertDataToType( val, resType)
            res[key] = resVal
        return res


    def schemalizeNoTime(self, jsonObj):
        res = deepcopy(jsonObj)
        for key, val in jsonObj.items():
            if val is None:
                del res[key]
                continue

            resVal = val
            resType = self._fieldTypeMap[key]
            if type(val) is not resType and resType is not datetime:
                resVal = self._convertDataToType( val, resType)
            res[key] = resVal
        return res

    def getDBSafeAttr(self, key):
        attrType = self._fieldTypeMap[key]
        if attrType is datetime:
            val = getattr(self, key)
            if val is not None:
                return val.isoformat()
            else:
                return None
        return getattr(self, key)

    def getDBSafeAttrMap(self):
        attrMap =  {}
        for field in self._fieldTypeMap.keys():
            fieldVal = self.getDBSafeAttr(field)
            if fieldVal is not None:
                attrMap[field] =  fieldVal
        return attrMap

    def getAttrs(self):
        return self._fieldTypeMap.keys()

    def getAttrMap(self):
        attrMap =  {}
        for field in self._fieldTypeMap.keys():
            attrMap[field] =  getattr(self, field)
        return attrMap

    def getKeyDict(self):
        return { self.key : getattr(self, self.key)}

    def __repr__(self):
        return str(self.getAttrMap())

    def __eq__(self, obj):
        return self.getAttrMap() == obj.getAttrMap()

    @classmethod
    def newItemId(cls, item):
        def randId():
            return ''.join(random.choices(string.ascii_uppercase, k=3))\
                + ''.join(random.choices(string.digits, k=4))

        newId = randId()
        itemTable = cls.getItemTable(item)
        tableKey = getattr( item, 'key')

        while True:
            response = itemTable.query(
                KeyConditionExpression=Key(tableKey).eq(newId)
            )
            if len(response['Items']) != 0:
                newId = randId()
            else:
                logger.info("Allocated id is :{}".format(newId))
                return newId


    @classmethod
    def getItemTable(cls, itemOrItemClass):
        className = itemOrItemClass.__class__.__name__
        if type(itemOrItemClass) is type:
            className = itemOrItemClass.__name__
        logger.info("Getting table: {}".format(className))
        return DBManager.table(className)

    @classmethod
    def addItem(cls, item, idGen=None):
        '''
            Use idGen to control the way id is generated
        '''
        itemTable = cls.getItemTable(item)
        tableKey = getattr( item, 'key')
        logger.info("Key are: {}".format(tableKey))
        # Generate a new item id
        newId = cls.newItemId(item)
        setattr( item, tableKey, newId)

        itemTable.put_item(
            Item=item.getDBSafeAttrMap()
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
        keyDict = item.getKeyDict()
        try:
            itemTable.delete_item(
                Key = keyDict
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
        for key in (set(item.getAttrs()) - set([item.key])):
            attrVal = item.getDBSafeAttr(key)
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
        if 'Item' not in response:
            logger.info("Requiring item: {} does not exist.".format(keys))
            return Errors.ErrorNoSuchId
        reItem = DBManager.toJsonData(response['Item'])
        logger.debug("getItem item: {}".format(reItem))
        return reItem

    @classmethod
    def getItemsByQuery(cls, specs, item):
        '''
            
        '''
        itemTable = cls.getItemTable(item)

        filterExp = None
        keyDict = {}
        sortSpec = None
        for spec in specs:
            attrName = spec['attr_name']
            attrVal = spec.get('attr_val')
            if attrName == item.key:
                if attrVal is not None:
                    keyDict[attrName] = attrVal
            else:
                #This is an filtering spec
                if attrVal is not None:
                    logger.info("Adding filtering exp: {},{}".format(attrName, attrVal))
                    if filterExp is not None:
                        filterExp &= Attr(attrName).eq(attrVal)
                    else:
                        filterExp = Attr(attrName).eq(attrVal)
            #This is an sorting spec
            if 'descending' in spec:
                sortSpec = spec

        keyExp = None
        for attrName, attrVal in keyDict.items():
            if keyExp is None:
                keyExp = Key(attrName).eq(attrVal)
            else:
                keyExp &= Key(attrName).eq(attrVal)
        queryKwargs = {}
        if keyExp is not None:
            queryKwargs['KeyConditionExpression'] = keyExp
        if filterExp is not None:
            queryKwargs['FilterExpression'] = filterExp

        try:
            response = itemTable.scan(**queryKwargs)
        except Exception as e:
            logger.exception(e)
            return Errors.ErrorRequestIllFormated
        # sorting
        items = sorted(
            DBManager.toJsonData(response['Items']),
            key = lambda item: item[sortSpec['attr_name']], reverse=sortSpec['descending']
        )

        logger.info("getItemsByQuery :{}".format(items))
        return items

    @classmethod
    def getItemsByIds(cls, itemIds, item):
        itemTable = cls.getItemTable(item)

        keyExp = None
        for itemId in itemIds:
            subKeyExp = None
            for keyName, keyVal in itemId.items():
                if subKeyExp is None:
                    subKeyExp = Key(keyName).eq(keyVal)
                else:
                    subKeyExp &= Key(keyName).eq(keyVal)
            if keyExp is None:
                keyExp = subKeyExp
            else:
                keyExp |= subKeyExp
        itemIdToSeq = { str(itemId) : idx for idx, itemId in enumerate(itemIds)}
        try:
            response = itemTable.query(KeyConditionExpression=keyExp)
        except Exception as e:
            logger.exception(e)
            return Errors.ErrorRequestIllFormated

        # sort items according to original id position
        items = sorted(
            DBManager.toJsonData(response['Items']),
            key = lambda oneitem: itemIdToSeq[str({ item.key : oneitem[item.key] })]
        )
        logger.info("getItemsByIds :{}".format(items))
        return items

