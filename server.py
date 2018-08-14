# -*- coding: utf-8 -*-
import os
from redis import Redis, ConnectionError
from flask import Flask, jsonify, request, json
import fileinput
import caa
"""
    server.py
    Center point of CAA Management System.
    Example usage: python server.py
    Authur:
        !!!! Add your name here in alphabeta order!!!!!
        Zhiyu Feng{@zf499@nyu.edu}
"""

class Credentials(object):
    def __init__(self, environment, host, port, password, swagger_host):
        self.environment = environment
        self.host = host
        self.port = port
        self.password = password
        self.swagger_host = swagger_host

def determine_credentials():
    if 'VCAP_SERVICES' in os.environ:
        services = json.loads(os.environ['VCAP_SERVICES'])
        redis_creds = services['rediscloud'][0]['credentials']
        if os.path.isfile("/.dockerenv"):
            return Credentials("Docker running in Bluemix",
                               redis_creds['hostname'],
                               int(redis_creds['port']),
                               redis_creds['password'],
                               "portfoliocontainer.mybluemix.net")
        else: # Bluemix only
            return Credentials("Bluemix",
                               redis_creds['hostname'],
                               int(redis_creds['port']),
                               redis_creds['password'],
                               "portfoliomgmt.mybluemix.net")
    else: # Vagrant
        if os.path.isfile("/.dockerenv"):
            return Credentials("Docker running in Vagrant", "redis", 6379, None, "localhost:5000")
        else: # Vagrant only
            return Credentials("Vagrant", "127.0.0.1", 6379, None, "localhost:5000")

def update_swagger_specification(swagger_host):
    spec_dir = os.path.dirname(__file__)
    if len(spec_dir): # Not docker container
        spec_dir += "/"
    spec_dir += "static/swagger/specification/"
    with open(spec_dir + "portfolioMgmt.json") as f:
        spec_lines = f.readlines()
    with open(spec_dir + "portfolioMgmt.js", 'w') as f:
        f.write("var spec = ")
        for i in range(len(spec_lines)):
            if '"host"' in spec_lines[i] and i < 20:
                pos = spec_lines[i].find('"host"')
                spec_lines[i] = spec_lines[i][:pos+6] + ': "'+swagger_host+'",\n'
            f.write(spec_lines[i])
        f.write(";")

def init_redis(hostname, port, password):
    global redis_server
    redis_server = Redis(host=hostname, port=port, password=password)
    try:
        redis_server.ping()
    except ConnectionError:
        raise RedisConnectionException()
    #remove_old_database_assets() # to remove once you ran it once on your Vagrant
    fill_database_assets() # to remove once you ran it once on your Vagrant

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    creds = determine_credentials()
    print " ~ Identified the environment as: "+creds.environment
    try:
        init_redis(creds.host, creds.port, creds.password)
    except RedisConnectionException:
        print "The server could not connect to Redis. Stopping...\n\n"
        exit(1)
    update_swagger_specification(creds.swagger_host)
    port = os.getenv('PORT', '5000')
    app.run(host='0.0.0.0', port=int(port), debug=True)
