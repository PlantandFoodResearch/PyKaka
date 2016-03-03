import csv
from urllib import request, parse
import re
import pandas as pd
from pymongo import MongoClient
import pql
import yaml


class Config:
    cfg = None
    def __init__(self, fn):
        s = open(fn, "r")
        self.cfg = yaml.load(s)

    def __getitem__(self,index):
        if index in self.cfg:
            return self.cfg[index]
        else:
            raise Exception("ERROR in kaka.py: Config not found in config.yml")


class Kaka:
    @staticmethod
    def qry_mongo(realm, qry, cfg=Config("config.yml")):
        host = cfg["mongo"]["host"]
        port = cfg["mongo"]["port"]

        client = MongoClient(host, port)
        db = client.primary
        coll = eval("db." + realm)
        qry = pql.find(qry)
        res = coll.find(qry)
        dat = []
        for d in res:
            dat.append(d)
        return pd.DataFrame(dat)

    @staticmethod
    def qry_pql(realm, expr, cfg=Config("config.yml")):
        if(re.search("[a-zA-Z0-9\\s\'\"]=[a-zA-Z0-9\\s\'\"]",expr)):
            print("ERROR: You seem to have a single = in your expression. If it is a comparison operator use ==.")
            return None
       
        host = cfg["web"]["host"]
        port = cfg["web"]["port"]

        qry_str = expr
        qry_str = "http://" + host + ":" + str(port) + "/qry/" + realm + "/?infmt=python&qry=%s" % qry_str
        print(qry_str)
        return pd.read_csv(qry_str)

    def qry(realm, expr, mode="pql", cfg=Config("config.yml")):
        if(mode == "pql"):
            return Kaka.qry_pql(realm, expr, cfg=cfg)
        else:
            return Kaka.qry_mongo(realm, expr, cfg=cfg)

