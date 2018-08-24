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
          "200": {
            "description": "Case id of the new case",
            "schema": {
              "$ref": "#/definitions/caseid_response"
            }
          }
        }
      },
      "put": {
        "summary": "Update an existing case",
        "description": "Update an existing case by providing a case. Id in that case refers to which case you are updating, any attribute with a non-null value will be updated",
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
            "description": "Case is updated sucessfully",
            "schema": {
              "$ref": "#/definitions/cases_response"
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
            "description": "Case is deleted succesfully",
            "schema": {
              "$ref": "#/definitions/cases_response"
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
              "$ref": "#/definitions/cases_response"
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
              "$ref": "#/definitions/cases_response"
            }
          }
        }
      }
    },
    "/case_status/": {
      "get": {
        "summary": "returns all defined case status",
        "tags": [
          "CaseStatus"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "schema": {
              "$ref": "#/definitions/casestatus_response"
            }
          }
        }
      }
    },
    "/usr/{usr_id}": {
      "get": {
        "summary": "get a usr's information by usrId",
        "parameters": [
          {
            "name": "usr_id",
            "in": "path",
            "required": true,
            "type": "integer"
          }
        ],
        "tags": [
          "User"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "schema": {
              "$ref": "#/definitions/usr"
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
    "caseStatus_id": {
      "type": "integer"
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
          "$ref": "#/definitions/caseStatus_id"
        }
      }
    },
    "case": {
      "type": "object",
      "properties": {
        "caseId": {
          "$ref": "#/definitions/case_id"
        },
        "usrId": {
          "$ref": "#/definitions/usr_id"
        },
        "custName": {
          "type": "string"
        },
        "custContact": {
          "type": "string"
        },
        "statusId": {
          "$ref": "#/definitions/caseStatus_id"
        },
        "createTime": {
          "type": "string"
        },
        "closeTime": {
          "type": "string"
        }
      }
    },
    "usr": {
      "type": "object",
      "properties": {
        "id": {
          "$ref": "#/definitions/usr_id"
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
    "error_type": {
      "type": "string",
      "enum": [
        "error_no_such_id",
        "error_request_ill_formated"
      ]
    },
    "caseid_response": {
      "type": "object",
      "properties": {
        "error": {
          "$ref": "#/definitions/error_type"
        },
        "content": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/case_id"
          }
        }
      }
    },
    "cases_response": {
      "type": "object",
      "properties": {
        "error": {
          "$ref": "#/definitions/error_type"
        },
        "content": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/case"
          }
        }
      }
    },
    "casestatus_response": {
      "type": "object",
      "properties": {
        "error": {
          "$ref": "#/definitions/error_type"
        },
        "content": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/case_status"
          }
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
    }
  }
};
