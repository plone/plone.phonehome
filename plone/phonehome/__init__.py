import StringIO, csv, hashlib
import logging
import socket
import uuid

import pkg_resources

import checker
from plone.phonehome.config import CALL_TIMEOUT, ConnectionProblem


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
    uid = getattr(app,'plonephonehomeid', None)
    if not uid:
        uid = uuid.uuid1().hex
        app.plonephonehomeid = uid
        import transaction
        transaction.commit()

    # Phone home
    timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(CALL_TIMEOUT)
    try:
        checker.checkVersions(uid, ws, wshash)
    except ConnectionProblem, e:
        logging.warning("Plone Phone Home connection failed with error: %s" % e)
    finally:
        socket.setdefaulttimeout(timeout)