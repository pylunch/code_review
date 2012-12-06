#from pyql import ingest
from pyql.ingest import update_database
from pyql.ingest import ingest_all
#from pyql.ingest import rebuild_database
#from pyql.ingest import reset_unlooked
#from pyql.ingest import visit_fix

import sqlite3
import os
import shutil

def setup():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    SQL = open('/grp/hst/wfc3a/Software/Trunk/Utilities/ql.sql').read()
    cursor.executescript(SQL)
    conn.close()

    if os.access('/grp/hst/wfc3a/unlooked/12689/VisitHA/', os.F_OK) != True:
        os.makedirs('/grp/hst/wfc3a/unlooked/12689/VisitHA/')
    shutil.copyfile('/grp/hst/wfc3a/Quicklook/12689/VisitHA/ibu9hadqq_flt.fits', 
        '/grp/hst/wfc3a/unlooked/12689/VisitHA/ibu9hadqq_flt.fits')
    file_dict = ingest_all.make_file_dict('/grp/hst/wfc3a/unlooked/12689/VisitHA/ibu9hadqq_flt.fits')
    update_database.update_database(file_dict, 'test.db')


class TestUpdateDatabase(object):
    '''
    '''

    def setup(self):
        conn = sqlite3.connect('test.db')
        self.cursor = conn.cursor()
        conn.text_factory = str

    def testMaster(self):
        self.cursor.execute('SELECT * FROM master')
        result = self.cursor.fetchall()[0]
        assert result[0] == 1
        assert result[1] == 'ibu9hadqq_flt.fits'
        assert result[2] == 'Oct 24 2012'
        assert result[3] == '/grp/hst/wfc3a/Quicklook/12689/VisitHA'
        assert result[4] == 'uvis_flt_0'
        assert result[5] == 'UVIS'
        assert result[6] == '6'
        assert result[7] == 'VisitHA-ibu9hadqq_flt.jpg'
        assert result[8] == '/grp/hst/wfc3a/Cal_Links/12689'
        assert result[9] == 'Oct 24 2012'
        assert result[10] == 'cal'

    def testAssociations(self):
        pass

def teardown():
    os.remove('test.db')
    os.remove('/grp/hst/wfc3a/unlooked/12689/VisitHA/ibu9hadqq_flt.fits')
