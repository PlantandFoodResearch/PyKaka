import csv
import re
import pandas as pd
from pymongo import MongoClient
import pql
import yaml
import sys


class Config:
    cfg = None
    def __init__(self, fn=None):
        if fn:
            s = open(fn, "r")
            self.cfg = yaml.load(s)
        else:
            self.cfg = {
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


def urlencode_qry(qry):
    print("Processing: " + qry)
    if sys.version_info >= (3, 0):
        from urllib import parse    
        return  parse.urlencode({"qry":qry, "infmt": "python"})
    elif sys.version_info > (2, 6) and sys.version_info  <  (3,0):
        import urllib
        return urllib.urlencode({"qry":qry, "infmt": "python"})
    else:
        raise Exception("PyKaka requires python > 2.6")


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

        qry_str = urlencode_qry(expr)
        qry_str = "http://" + host + ":" + str(port) + "/qry/" + realm + "/?%s" % qry_str
        print(qry_str)
        return pd.read_csv(qry_str)

    @staticmethod
    def qry(realm, expr, mode="pql", columns = None, cfg=Config()):
        if(mode == "pql"):
            dat = Kaka.qry_pql(realm, expr, cfg=cfg)
        else:
            dat = Kaka.qry_mongo(realm, expr, cfg=cfg)

        if columns:
            return pd.DataFrame(dat, columns=columns)
        else:
            return dat

    @staticmethod
    def send(realm, config, data):
        pass
