import csv
from urllib import request, parse
import re
import pandas as pd
from pymongo import MongoClient
import pql
import yaml


class Config:
    cfg = None
    def __init__(self, fn=None):
        if fn:
            s = open(fn, "r")
            self.cfg = yaml.load(s)
        else:
            cfg = {
                'mongo_host':'mongo',
                'mongo_port': 27017,
                'web_host': 'web',
                'web_port': 80,
            }


    def __getitem__(self,index):
        if index in self.cfg:
            return self.cfg[index]
        else:
            raise Exception("ERROR in kaka.py: Config not found in config.yml")


class Kaka:
    @staticmethod
    def qry_mongo(realm, qry, cfg=Config()):
        host = cfg["mongo_host"]
        port = cfg["mongo_port"]

        client = MongoClient(host, port)
        db = client["primary"]
        try:
            coll = db[realm]
        except:
            raise Exception("realm not found")
        qry = pql.find(qry)
        res = coll.find(qry)
        dat = []
        for d in res:
            dat.append(d)
        return pd.DataFrame(dat)

    @staticmethod
    def qry_pql(realm, expr, cfg=Config()):
        if(re.search("[a-zA-Z0-9\\s\'\"]=[a-zA-Z0-9\\s\'\"]",expr)):
            print("ERROR: You seem to have a single = in your expression. If it is a comparison operator use ==.")
            return None
       
        host = cfg["web_host"]
        port = cfg["web_port"]

        qry_str = expr
        qry_str = "http://" + host + ":" + str(port) + "/qry/" + realm + "/?infmt=python&qry=%s" % qry_str
        print(qry_str)
        return pd.read_csv(qry_str)

    def qry(realm, expr, mode="pql", cfg=Config("config.yml")):
        if(mode == "pql"):
            return Kaka.qry_pql(realm, expr, cfg=cfg)
        else:
            return Kaka.qry_mongo(realm, expr, cfg=cfg)

