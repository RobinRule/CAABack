
from .DBManager import DBManager
from boto3.dynamodb.conditions import Key, Attr
from global_var import Errors 
from datetime import datetime
from dateutil.parser import parse as timeParse
from copy import deepcopy

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
        self._keys = [ key[0] for key in fieldList[0] ]
        
        fieldList = fieldList[1:] + fieldList[0]
        
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
        for key in (set(item.getAttrs()) - set(item.getKeys())):
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
            return None
        reItem = DBManager.toJsonData(response['Item'])
        logger.debug("Returning item: {}".format(keys))
        return reItem

    @classmethod
    def getItems(cls, specs, item):
        '''
            
        '''
        itemTable = cls.getItemTable(item)
        keys = item.getKeys()

        filterExp = None
        keyDict = {}
        sortSpecs = []
        for spec in specs:
            attrName = spec['attr_name']
            attrVal = spec.get('attr_val')
            if attrName in keys:
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
                sortSpecs.append(spec)

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
            response = itemTable.query(**queryKwargs)
        except Exception as e:
            logger.exception(e)
            return Errors.ErrorRequestIllFormated
        #TODO: sorting

        return DBManager.toJsonData(response['Items'])