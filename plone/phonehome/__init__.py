import StringIO, csv, hashlib
import logging
import socket
import uuid

import pkg_resources
from zope.exceptions import UserError

import checker
from interfaces import CALL_TIMEOUT


# CHECK_URL = 'http://localhost:9999/check?uid=%s&hash=%s'
# UPDATE_URL = 'http://localhost:9999/update'

CHECK_URL = 'http://plonephonehome.appspot.com/check?uid=%s&hash=%s'
UPDATE_URL = 'http://plonephonehome.appspot.com/update'


CALL_TIMEOUT = 5

OKCODE = 'OK' # everything is ok
UPDATECODE = 'UPDATE' # hash has changes, requires to send full info
FAILEDCODE = 'FAILED' # check-in procedure failed


class ConnectionProblem(UserError):
    pass


def initialize(context):
    # build environment description
    workingset = [(dist.project_name, dist.version) for dist in 
                  pkg_resources.working_set]
    workingset.sort()

    out = StringIO.StringIO()
    writerow = csv.writer(out).writerow

    [writerow(row) for row in workingset]

    ws = out.getvalue()
    wshash = hashlib.md5(ws).hexdigest()

    # checker.setWorkingsetInfo(ws, wshash)

    # Check for existing uid, otherwise, create a new one
    import Zope2
    app = Zope2.app()
    uid = getattr(app,'uid', None)
    if not uid:
        uid = uuid.uuid1().hex
        app.uid = uid
        import transaction
        transaction.commit()

    # Phone home
    timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(CALL_TIMEOUT)
    try:
        checker.checkVersions(uid, ws, wshash)
    except ConnectionProblem, e:
        logging.warning("Phone Home connection failed with error: %s" % e)
    finally:
        socket.setdefaulttimeout(timeout)