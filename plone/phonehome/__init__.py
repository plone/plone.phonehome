import StringIO, csv, hashlib
import logging
import socket
import uuid

import pkg_resources

import checker
from plone.phonehome.config import CALL_TIMEOUT, ConnectionProblem


logger = logging.getLogger('plone.phonehome')

def getDebugModeStatus():
    # TODO Does this cover all options?
    try:
        from Products.Five.fiveconfigure import debug_mode
        return debug_mode
    except ImportError:
        from App.config import getConfiguration
        return getConfiguration().debug_mode


def initialize(context):
    # Don't run if Zope is running in Debug Mode.
    if not getDebugModeStatus():
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
            try:
                import transaction
                transaction.commit()
            except ConflictError:
                pass # Ignore
            
        # Phone home
        timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(CALL_TIMEOUT)
        logger.info("Connecting to plone.phonehome service.")
        try:
            checker.checkVersions(uid, ws, wshash)
        except ConnectionProblem, e:
            logger.warning("plone.phonehome connection failed with error: %s" % e)
        else:
            logger.info("Connection complete.")
        finally:
            socket.setdefaulttimeout(timeout)