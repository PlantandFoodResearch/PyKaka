# -*- coding: utf-8 -*-

########################
## Algorithms is a concept from C++ (STL http://www.sgi.com/tech/stl/). It allows 
## Looping through lists without having to write teh actual loop again and again
## and tehrefore follows the DNRY paradigm. 
## You define an operator which will be applied to a list item.
########################

class traverse:
    last = None

    def __call__(self, lst, op):
        for item in lst:
            item = op(item, self.last)
            self.last = item
        return lst


class count:
    ct = 0

    def __call__(self, lst, comp, op=None):
        for item in lst:
            if(op):
                if(op(item, comp)):
                    self.ct += 1
            else:
                if(item == comp):
                    self.ct += 1
        return self.ct


def find(lst, comp, op=None):
    for item in lst:
        if(op):
            if(op(item, comp)):
                return item
        else:
            if(item == comp):
                return item
    return None


def for_each(lst, op):
    for item in lst:
        item = op(item)
    return lst


def accumulate(lst, op, tgt, ret=True):
    for item in lst:
        tgt = op(item, tgt)
    return tgt


def acc_validate(lst, op, op_val, tgt, ret=True):
    for item in lst:
        op_val(item, tgt)
        tgt = op(item, tgt)
    return tgt


def propagate(lst, op, tgt1, tgt2):
    for item in lst:
        tgt1, tgt2 = op(item, tgt1, tgt2)
    return tgt1, tgt2


# import data serializers
import gzip
import csv
import xlrd
import json
import pandas
import vcf


############################
## Data connectors are building on teh algoirthms defined in algorithms.py.
## These connectors see data as list of rows the connector loops through and
## apllies an operator on the row of data.
## There are foulr classes inhertiting from Data Connector:
## ExcelConnector
## CsvConnector
## DictListConnector
## The aim is to give the programmer teh abilitity to write an e.g. import operator for data which can be aplied
## to different input data formats.
############################

class DataConnector:
    name = 'None'
    header = None
    head_mapper = None
    current = None
    origin_name = None

    def __init__(self):
        pass

    def __next__(self):
        pass

    def next(self):
        return self.__next__()

    def all(self):
        pass

    def close(self):
        pass


class ExcelConnector(DataConnector):
    fn = None
    sheet_name = None
    sheet = None
    curr_row = 0
    max_row = 0
    header = None

    def __init__(self, fn, sheet_name=None):
        self. fn = fn
        self.sheet_name = sheet_name
        self.load()

    def __iter__(self):
        return self

    def __next__(self):
        num_rows = self.sheet.nrows - 1
        self.curr_row += 1
        if(self.curr_row < num_rows):
            r = self.sheet.row_values(self.curr_row)
            return dict(list(zip(self.header, r)))
        else:
            raise StopIteration

    def load(self):
        workbook = xlrd.open_workbook(self.fn)
        if self.sheet_name:
            self.sheet = workbook.sheet_by_name(self.sheet_name)
        else:
            sheet_names = workbook.sheet_names()
            self.sheet = workbook.sheet_by_name(sheet_names[0])

        self.header = self.get_header()

    def get_header(self):
        return self.sheet.row_values(0)

    def all(self):
        res = []
        for r in self:
            res.append(r)

        return res

    @staticmethod
    def GetSheets(fn):
        workbook = xlrd.open_workbook(fn)
        return workbook.sheet_names()


class CsvConnector(DataConnector):
    reader = None
    f = None
    gzipped = False
    delimiter = ','
    header = None

    def __init__(self, fn, delimiter=',', gzipped=False, header=None):
        self.origin_name = fn
        self.gzipped = gzipped
        self.delimiter = delimiter
        self.header=header
        self.load()

    def __iter__(self):
        return self

    def load(self):
        if(self.gzipped):
            self.f = gzip.open(self.origin_name, 'rt')
        else:
            self.f = open(self.origin_name, 'rt')
            
        self.reader = csv.DictReader(self.f, delimiter=self.delimiter, fieldnames=self.header)
        self.header = self.reader.fieldnames

    def __next__(self):
        self.current = next(self.reader)
        if(self.current):
            return self.current
        else:
            raise StopIteration

    def all(self):
        d = []
        for row in self:
            d.append(row)
        return d

    def close(self):
        self.f.close()


class DictListConnector(DataConnector):
    header = None
    lst = None

    def __init__(self, lst, expand_obs=False):
        self.lst = lst

        if expand_obs:
            self.lst, self.header = self.convert_obs_json()
        else:
            self.header = list(self.lst[0].keys())
        self.current = iter(self.lst)

    def make_fields_from_json(self, s, b, header, field):
        # Add obs fields to new list
        if field in s:
            # Get the json content
            a_values = json.loads(s[field])

            for a in a_values:
                if a not in header:
                    header.append(a)
                b[a] = a_values[a]

        return b

    def convert_obs_json(self):        
        # Check is objects have an obs field
        header = []
        #if 'obs' in test:
        res = []
        # Browse through list of records
        for s in self.lst:
            b = OrderedDict()
            # Add sql fields to new list
            for r in s:
                if r not in ["obs","obs1","obs2", "values"]:
                    if r not in header:
                        header.append(r)
                    b[r] = s[r]

            # Add obs fields to new list
            if 'obs' in s:
                b = self.make_fields_from_json(s, b, header, 'obs')

            if 'values' in s:
                b = self.make_fields_from_json(s, b, header, 'values')

            if 'obs1' in s:
                b = self.make_fields_from_json(s, b, header, 'obs1')

            if 'obs2' in s:
                b = self.make_fields_from_json(s, b, header, 'obs2')

            res.append(b)

        return res, header


    def load(self):
        pass

    def rename(self, row, tgt):

        if not(self.head_mapper):
            return row

        n_row = dict(
            (self.head_mapper[key], value) for (key, value) in list(row.items())
            )

        tgt.append(n_row)
        return tgt

    def reload(self, new_header):
        self.head_mapper = dict(list(zip(self.header, new_header)))
        self.header = new_header
        lst = []
        self.lst = accumulate(self, self.rename, lst)

    def __iter__(self):
        return self

    def __next__(self):
        cur = next(self.current)
        if(cur):
            return cur
        else:
            raise StopIteration

    def all(self):
        return self.lst

    def close(self):
        del self.lst


class PandasConnector(DataConnector):
    header = None
    df = None
    current = None

    def __init__(self, df):
        if(type(df)==pandas.DataFrame):
            self.df = df
        if(type(df)==dict): 
            self.df = pd.DataFrame(df)
        self.current = iter(self.df.iterrows())
        self.header = df.columns.values

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        cur = next(self.current)
        if(cur):
            return cur[1]
        else:
            raise StopIteration

    def all(self):
        return self.df.to_dict(orient="records")

    def close():
        pass

class PandasConnector(object):
    header = None
    df = None
    current = None

    def __init__(self, df):
        if(type(df)==pandas.DataFrame):
            self.df = df
        if(type(df)==dict):
            self.df = pd.DataFrame(df)
        self.current = iter(self.df.iterrows())
        self.header = df.columns.values

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        cur = next(self.current)
        if(cur):
            return cur[1]
        else:
            raise StopIteration

    def all(self):
        return self.df.to_dict(orient="records")

    def close():
        pass

def collect_samples(sample, r):
    dat = sample.data._asdict()
    for d in dat:
        ind = sample.sample + '__' + d
        r[ind] = str(dat[d])
    return r

def collect(record,res):
    r = {}
    r['CHROM'] = record.CHROM
    r['POS'] = record.POS
    r['REF'] = record.REF
    r['ALT'] = str(record.ALT)
    r['FORMAT'] = record.FORMAT
   
    r = accumulate(record.samples, collect_samples, r)

    res.append(r)
    return res


class VcfConnector(PandasConnector):
    def __init__(self, fn):
        vc = vcf.Reader(open(fn,'r'))
        res = []
        res = accumulate(vc, collect, res)
        pd = pandas.DataFrame(res)
        super(VcfConnector, self).__init__(pd)
























