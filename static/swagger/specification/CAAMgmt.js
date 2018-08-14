var spec = {
  "swagger": "2.0",
  "info": {
    "title": "CAA Mgmt Project",
    "description": "API for CAA management",
    "version": "1.0"
  },
  "host": "portfoliomgmt.mybluemix.net",
  "schemes": [
    "https",
    "http"
  ],
  "basePath": "/api/v1",
  "produces": [
    "application/json"
  ],
  "paths": {
    "/case/": {
      "post": {
        "summary": "Create a new case",
        "description": "Create a new case",
        "parameters": [
          {
            "name": "case_id",
            "in": "path",
            "description": "an integer id of case",
            "required": true,
            "type": "string",
            "default": "0"
          }
        ],
        "tags": [
          "Cases"
        ],
        "responses": {
          "201": {
            "description": "Case id of the new case",
            "schema": {
              "type": "integer",
              "description": "an integer id of case"
            }
          },
          "400": {
            "description": "Body is not well formed (more details in error message)",
            "schema": {
              "$ref": "#/definitions/error_data"
            }
          }
        }
      }
    },
    "/case/{case_id}": {
      "get": {
        "summary": "Get case by id",
        "description": "This get request returns a case by the id specified",
        "parameters": [
          {
            "name": "case_id",
            "in": "path",
            "description": "an integer id of case",
            "required": true,
            "type": "string",
            "default": "0"
          }
        ],
        "tags": [
          "Cases"
        ],
        "responses": {
          "200": {
            "description": "A case",
            "schema": {
              "type": "object",
              "items": {
                "$ref": "#/definitions/case"
              }
            }
          }
        }
      }
    }
  },
  "definitions": {
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