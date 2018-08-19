var spec = {
  "swagger": "2.0",
  "info": {
    "title": "CAA Mgmt Project",
    "description": "API for CAA management",
    "version": "1.0"
  },
  "host": "localhost:5000",
  "schemes": [
    "https"
  ],
  "basePath": "/api/v1",
  "produces": [
    "application/json"
  ],
  "paths": {
    "/cases": {
      "post": {
        "summary": "Create a new case",
        "description": "Create a new case",
        "parameters": [
          {
            "name": "case",
            "in": "body",
            "description": "a case needed to be added to database",
            "required": true,
            "schema": {
              "$ref": "#/definitions/case"
            }
          }
        ],
        "tags": [
          "Cases"
        ],
        "responses": {
          "201": {
            "description": "Case id of the new case",
            "schema": {
              "$ref": "#/definitions/case_id"
            }
          },
          "400": {
            "description": "Body is not well formed (more details in error message)",
            "schema": {
              "$ref": "#/definitions/error_data"
            }
          }
        }
      },
      "put": {
        "summary": "Update an existing case",
        "description": "Update an existing case by providing a case. Id in that case refers to which case you are updating, any attribute with a non-null value will be Update",
        "parameters": [
          {
            "name": "case",
            "in": "body",
            "description": "an integer id of case",
            "required": true,
            "schema": {
              "$ref": "#/definitions/case"
            }
          }
        ],
        "tags": [
          "Cases"
        ],
        "responses": {
          "200": {
            "description": "Case is updated sucessfully"
          },
          "404": {
            "description": "Case not found",
            "schema": {
              "$ref": "#/definitions/error_casedoesnotexist"
            }
          }
        }
      }
    },
    "/cases/{case_id}": {
      "delete": {
        "summary": "delete a case by id",
        "description": "delete a case refers by the given case id",
        "tags": [
          "Cases"
        ],
        "parameters": [
          {
            "name": "case_id",
            "in": "path",
            "description": "an integer id of case",
            "required": true,
            "type": "integer"
          }
        ],
        "responses": {
          "200": {
            "description": "Case is deleted succesfully"
          },
          "404": {
            "description": "No case with given case id exist (more details in error message)",
            "schema": {
              "$ref": "#/definitions/error_casedoesnotexist"
            }
          }
        }
      },
      "get": {
        "summary": "Get a case by id",
        "description": "This get request returns a case by the id specified",
        "parameters": [
          {
            "name": "case_id",
            "in": "path",
            "description": "an integer id of case",
            "required": true,
            "type": "integer"
          }
        ],
        "tags": [
          "Cases"
        ],
        "responses": {
          "200": {
            "description": "Case founded",
            "schema": {
              "type": "object",
              "items": {
                "$ref": "#/definitions/case"
              }
            }
          },
          "404": {
            "description": "Case not found",
            "schema": {
              "$ref": "#/definitions/error_casedoesnotexist"
            }
          }
        }
      }
    },
    "/cases/usr_id/{usr_id}/": {
      "get": {
        "description": "Search for usr's cases by id. By default the result is sorted by create time. User of this api can pass in a list of search specs to further refine the result. Relationship between different search spec is AND. In each search spec, you can specify the a specified val for the attr that you are searching for or you can specify you want the sorting order of returned result. When multiple sorting order is specified, the one appears first takes a higher priority. An usr is only allowed to search his own cases and his team members' cases.",
        "tags": [
          "Cases"
        ],
        "parameters": [
          {
            "name": "usr_id",
            "in": "path",
            "required": true,
            "type": "integer"
          },
          {
            "name": "search_specs",
            "in": "body",
            "required": false,
            "schema": {
              "type": "array",
              "items": {
                "$ref": "#/definitions/search_spec"
              }
            }
          }
        ],
        "responses": {
          "200": {
            "description": "An array of cases",
            "schema": {
              "type": "array",
              "items": {
                "$ref": "#/definitions/case"
              }
            }
          },
          "404": {
            "description": "Usr with given usr id does not existed",
            "schema": {
              "$ref": "#/definitions/error_casedoesnotexist"
            }
          }
        }
      }
    }
  },
  "definitions": {
    "case_id": {
      "type": "integer"
    },
    "usr_id": {
      "type": "integer"
    },
    "case": {
      "type": "object",
      "properties": {
        "caseId": {
          "type": "integer"
        },
        "usrId": {
          "type": "integer"
        },
        "custId": {
          "type": "integer"
        },
        "status": {
          "type": "string"
        },
        "createTime": {
          "type": "string"
        },
        "closeTime": {
          "type": "string"
        }
      }
    },
    "case_status": {
      "type": "object",
      "properties": {
        "nexts": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "str_val": {
          "type": "string"
        },
        "id": {
          "type": "integer"
        }
      }
    },
    "usr": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer"
        },
        "name_first": {
          "type": "string"
        },
        "name_last": {
          "type": "string"
        },
        "contacts": {
          "type": "string"
        }
      }
    },
    "search_spec": {
      "type": "object",
      "properties": {
        "attr_name": {
          "type": "string"
        },
        "attr_val": {
          "type": "string"
        },
        "descending": {
          "type": "boolean"
        }
      }
    },
    "error_data": {
      "type": "object",
      "properties": {
        "error": {
          "type": "string",
          "description": "Highlights that the data is not JSON or does not have the necessary required information.",
          "default": "The data is not valid."
        }
      }
    },
    "error_userexists": {
      "type": "object",
      "properties": {
        "error": {
          "type": "string",
          "description": "The user already exists in the database",
          "default": "The user already exists in the database."
        }
      }
    },
    "error_userdoesnotexist": {
      "type": "object",
      "properties": {
        "error": {
          "type": "string",
          "description": "The user does not exist in the database",
          "default": "The user does not exist in the database."
        }
      }
    },
    "error_casedoesnotexist": {
      "type": "object",
      "properties": {
        "error": {
          "type": "string",
          "description": "The case does not exist in the database",
          "default": "The case does not exist in the database."
        }
      }
    },
    "error_caseexists": {
      "type": "object",
      "properties": {
        "error": {
          "type": "string",
          "description": "Case with id x already existed",
          "default": "Case with id x already existed."
        }
      }
    }
  }
};
