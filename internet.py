#!/usr/bin/python
"""
internet.py
TODO:
write documentation in detail
"""
import slog
import urllib2
"""
Check availability of Internet Connection
"""
def internet_on():
    """
    Try to open a random url if error occured
    to check internet connection availability
    """
    try:
        response=urllib2.urlopen('http://74.125.113.99',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False


a = internet_on()
slog.info('Internet  ' + str(a))
if __name__ == '__main__':
	pass
