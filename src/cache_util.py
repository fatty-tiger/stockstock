import json


class StockInfoCache:
    def __init__(self):
        self._load_stock2name()

    def _load_stock2name(self):
        self.name2code = {}
        self.code2name = {}
        with open('data/all_stocks.json') as f:
            d = json.load(f)
            all_idxs = d['ts_code'].keys()
            for k in all_idxs:
                ts_code = d['ts_code'][k]
                ts_name = d['name'][k]
                self.name2code[ts_name] = ts_code
                self.code2name[ts_code] = ts_name
    
    def get_code_by_name(self, name):
        return self.name2code[name]

    def get_name_by_code(self, name):
        return self.name2code[name]
    

            