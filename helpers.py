""" Module that contains python helper functions to add the necessary functionality
of PHP for port to be as close as it possible to the original version as well as
cross-version implementations of various detectors/parsers
"""

# cross-version import of urlparse to break URL
# strings up in components
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


def empty(lst, key):
    """Check whether input key is absent or 0/None/""
    in the input list. The functionality is similar
    to PHP's empty() function so read PHP docs to
    know more

    :param lst: list Input list to check in
    :param key: string Input key to check for
    :return: bool Empty or not
    """
    try:
        # try to get the value with the key
        # and evaluate it as a boolean
        return not bool(lst[key])
    except KeyError:
        # if there is no such key in the list
        # return True therefore the value is
        # assumed to be empty (as in PHP)
        return True


def detect_url_scheme(url):
    """ Return a protocol that is used to access the input URL

    :param url: string URL to grab protocol from
    :return: string Protocol
    """
    return urlparse.urlparse(url).scheme


def detect_url_netloc(url):
    """Return a base part of a link (url netloc)

    :param url: string URL to grab a base part from
    :return: string Base part of the URL
    """
    return urlparse.urlparse(url).netloc


def detect_url_query(url):
    """Return a query part of a passed in link

    :param url: string URL to grab a query part from
    :return: string Query part of the URL
    """
    return urlparse.urlparse(url).query


def parse_qs_wrap(string):
    """return parsed query (wrapper for cross-version support)

    :param string: string Querystring
    :return: dictionary of query vars
    """
    return urlparse.parse_qs(string)


def is_relative_base(url):
    """Detect whether the input url consists only from scheme and netloc

    :param url: string URL to validate
    :return: bool Is URL consists from scheme and netloc only (is relative base)
    """
    parsed = urlparse.urlparse(url)
    return True if parsed.scheme and parsed.netloc and not \
        (parsed.path and parsed.params and parsed.query and parsed.fragment) else False


def is_absolute_base(url):
    """Detects whether the input url has at least scheme and netloc (isAbsoluteBase)

    :param url: string URL to validate
    :return: bool Is URL consists at least from scheme and netloc only (is absolute base)
    """
    parsed = urlparse.urlparse(url)
    return True if parsed.scheme and parsed.netloc else False


def get_absolute_base(url):
    """Return absolute base of a passed in link (scheme and netloc) with a trailing slash at the end "/"

    :param url: string URL to grab absolute base from
    :return: string Absolute base of the URL
    """
    parsed = urlparse.urlparse(url)
    return "%s://%s/" % (parsed.scheme, parsed.netloc)


def static_vars(**kwargs):
    """The workaround to add php's static function variables functionality to
    python functions. It's a decorator.

    :param kwargs: arbitrary amount of mixed variables
    :return: decorated function
    """

    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


def isset(lst, key, subkey=None):
    """Check for a passed key presence in a passed in dictionary. Also check for a sub key presence (key
    of a dict that is a value of a first passed in key)

    :param lst: list List to check for a key in
    :param key: string Key to check for
    :param subkey: string Subkey to check for
    :return: bool Is both specified key are present in a list?
    """
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


def un_camel(x):
    """Convert camel-styled string to underscore-style string

    :param x: string Camel-cased string
    :return: string Underscore-styled string
    """
    final = ''
    for item in x:
        if item.isupper():
            final += "_"+item.lower()
        else:
            final += item
    if final[0] == "_":
        final = final[1:]
    return final
