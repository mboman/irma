from irma.database.nosqlhandler import NoSQLDatabase
from bson import ObjectId
from irma.common.exceptions import IrmaDatabaseError


class FileObject(object):
    _uri = None
    _dbname = None
    _collection = None

    def __init__(self, dbname=None, id=None):
        if dbname:
            self._dbname = dbname
        self._dbfile = None
        self._id = None
        if id:
            self._id = ObjectId(id)
            self.load()

    def load(self):
        db = NoSQLDatabase(self._dbname, self._uri)
        self._dbfile = db.get_file(self._dbname, self._collection, self._id)

    def save(self, data, name):
        db = NoSQLDatabase(self._dbname, self._uri)
        self._id = db.put_file(self._dbname, self._collection, data, name)
        # refresh _dbfile field
        self.load()

    def delete(self):
        db = NoSQLDatabase(self._dbname, self._uri)
        db.delete_file(self._dbname, self._collection, self._id)

    @property
    def data(self):
        """Get the data"""
        if self._dbfile is None:
            raise IrmaDatabaseError("File has no data")
        return self._dbfile.read()

    @property
    def id(self):
        """Return str version of ObjectId"""
        if self._id is None:
            return None
        else:
            return str(self._id)
