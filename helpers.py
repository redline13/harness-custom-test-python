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
def detect_url_scheme(url):
    return urlparse.urlparse(url).scheme


# TODO: docstringify
# returns a base part of a link (url netloc)
# given an url as input
def detect_url_netloc(url):
    return urlparse.urlparse(url).netloc


# TODO: docstringify
# return a query part of a passed in link
def detect_url_query(url):
    return urlparse.urlparse(url).query


# TODO: docstringify
# return parsed query (wrapper
# for cross-version support)
def parse_qs_wrap(str):
    return urlparse.parse_qs(str)


# TODO: docstringify
# detects whether the input url consists
# only from scheme and netloc
def is_relative_base(url):
    parsed = urlparse.urlparse(url)
    return True if parsed.scheme and parsed.netloc and not \
                (parsed.path and parsed.params and parsed.query and parsed.fragment) else False


# TODO: docstringify
# detects whether the input url has
# al least scheme and netloc (isAbsoluteBase)
def is_absolute_base(url):
    parsed = urlparse.urlparse(url)
    return True if parsed.scheme and parsed.netloc else False


# TODO: docstringify
# returns absolute base of a passed in link
# (scheme and netloc) + /
def get_absolute_base(url):
    parsed = urlparse.urlparse(url)
    return "%s://%s/" % (parsed.scheme, parsed.netloc)


# TODO: docstringify
# the workaround to add php's static
# function variables functionality to
# python functions. It's a decorator.
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


# TODO: docstringify
# isset() function to check for a passed
# key presence in a passed in dictionary.
# Also check for a sub key presence (key
# of a dict that is a value of a first
# passed in key)
def isset(lst, key, subkey = None):
    try:
        lst[key]
        if subkey:
            try:
                lst[key][subkey]
            except TypeError:
                return False
        return True
    except KeyError:
        return False
