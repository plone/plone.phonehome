# CHECK_URL = 'http://localhost:9999/check?uid=%s&hash=%s'
# UPDATE_URL = 'http://localhost:9999/update'

CHECK_URL = 'http://plonephonehome.appspot.com/check?uid=%s&hash=%s'
UPDATE_URL = 'http://plonephonehome.appspot.com/update'


CALL_TIMEOUT = 5

OKCODE = 'OK' # everything is ok
UPDATECODE = 'UPDATE' # hash has changes, requires to send full info
FAILEDCODE = 'FAILED' # check-in procedure failed


from zope.exceptions import UserError

class ConnectionProblem(UserError):
    pass
