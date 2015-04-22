from django.db import connection
import random
import string
import hashlib
import time
import hmac


#Functions to create hash of the password
def makeSalt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def hashPassword(name, password, salt=""):
    if not salt:
        salt = makeSalt()
    h = hashlib.sha256(name + password + salt).hexdigest()
    return '%s,%s' % (h, salt)

def validPassword(name, password, h):
    return h == hashPassword(name, password, h.split(',')[1])

#Functions to store and validate cookies
SECRET = 'InFoRmAtIoN'
def hashStr(s):
    return hmac.new(SECRET, s).hexdigest()

def makeSecureVal(s):
    return "%s|%s" % (s, hashStr(s))

def checkSecureVal(h):
    val = h.split('|')[0]
    if h == makeSecureVal(val):
        return val
    return None

def setCookie(response, password):
    cursor = connection.cursor()
    getUserSql = "SELECT userId FROM userModule_user WHERE password = %s"
    cursor.execute(getUserSql, [password, ])
    row = cursor.fetchone()
    if row:
	response.set_cookie('sessionId', makeSecureVal(str(row[0])))

def validateCookie(request):
    if "sessionId" in request.COOKIES:
        return checkSecureVal(request.COOKIES["sessionId"])
    return None
