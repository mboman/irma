import config
from lib.irma.database.nosqlobjects import NoSQLDatabaseObject
from lib.irma.fileobject.handler import FileObject
from datetime import datetime

cfg_dburi = config.get_db_uri()
cfg_dbname = config.frontend_config['mongodb'].dbname
cfg_coll = config.frontend_config['collections']

class ScanStatus:
    init = 10
    launched = 11
    finished = 20
    cancelling = 30
    cancelled = 31

    label = {
             init:"scan created",
             launched:"scan launched",
             finished:"scan finished",
             cancelled:"scan cancelled"
    }

class ScanInfo(NoSQLDatabaseObject):
    _uri = cfg_dburi
    _dbname = cfg_dbname
    _collection = cfg_coll.scan_info

    def __init__(self, dbname=None, id=None):
        if dbname:
            self._dbname = dbname
        self.user = None
        self.date = datetime.now()
        self.oids = {}
        self.probelist = None
        self.status = ScanStatus.init
        super(ScanInfo, self).__init__(id=id)

    def get_results(self):
        res = {}
        for (oid, name) in self.oids.items():
            r = ScanResults(id=oid)
            if self.probelist is not None:
                res[name] = dict((k, v) for (k, v) in r.results.iteritems() if k in self.probelist)
            else:
                res[name] = dict((k, v) for (k, v) in r.results.iteritems())
        return res

class ScanResults(NoSQLDatabaseObject):
    _uri = cfg_dburi
    _dbname = cfg_dbname
    _collection = cfg_coll.scan_results

    def __init__(self, dbname=None, id=None):
        if dbname:
            self._dbname = dbname
        self.probelist = []
        self.results = {}
        super(ScanResults, self).__init__(id=id)

class ScanFile(FileObject):
    _uri = cfg_dburi
    _dbname = cfg_dbname
    _collection = cfg_coll.scan_files
