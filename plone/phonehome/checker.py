import urllib, urllib2

from plone.phonehome.config import ConnectionProblem
from plone.phonehome.config import CHECK_URL, UPDATE_URL
from plone.phonehome.config import OKCODE, UPDATECODE, FAILEDCODE

workingset = ''
workingset_hash = ''


def setWorkingsetInfo(ws, wshash):
    global workingset, workingset_hash
    workingset = ws
    workingset_hash = wshash


def checkVersions(uid, workingset, workingset_hash):
    try:
        response = urllib.urlopen(CHECK_URL%(uid, workingset_hash))
        data = response.read()
    except Exception, e:
        raise ConnectionProblem(str(e))

    code, message = data.split('\n', 1)
    
    if code in (OKCODE, FAILEDCODE):
        return code, message

    values = {'data' : workingset,
              'hash' : workingset_hash,
              'uid' : uid }

    data = urllib.urlencode(values)
    req = urllib2.Request(UPDATE_URL, data)

    try:
        response = urllib2.urlopen(req)
        respdata = response.read() 
    except Exception, e: 
        raise ConnectionProblem(str(e))

    return respdata.split('\n', 1)
