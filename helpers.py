# module that contains python helper functions to add the necessary functionality
# of PHP for port to be as close as it possible to the original version as well as
# cross-version implementations of various detectors/parsers


# cross-version import of urlparse to break URL
# strings up in components
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


# TODO: docstringify
# checks whether input key is ebsent or 0/None/""
# in the input list. The functionality is similar
# to PHP's empty() function so read PHP docs to
# know more
def empty(lst, key):
    try:
        # try to get the value with the key
        # and evaluate it as a boolean
        return not bool(lst[key])
    except KeyError:
        # if there is no such key in the list
        # return True therefore the value is
        # assumed to be empty (as in PHP)
        return True


# TODO: docstringify
# returns a protocol that is used to access
# the input url
def detectUrlScheme(url):
    return urlparse.urlparse(url).scheme


# TODO: docstringify
# returns a base part of a link (url netloc)
# given an url as input
def detectUrlNetloc(url):
    return urlparse.urlparse(url).netloc


# TODO: docstringify
# detects whether the input url consists
# only from scheme and netloc
def isRelativeBase(url):
    parsed = urlparse.urlparse(url)
    return True if parsed.scheme and parsed.netloc and not \
                (parsed.path and parsed.params and parsed.query and parsed.fragment) else False


# TODO: docstringify
# detets whether the input url has
# al least scheme and netloc (isAbsoluteBase)
def isAbsoluteBase(url):
    parsed = urlparse.urlparse(url)
    return True if parsed.scheme and parsed.netloc else False
