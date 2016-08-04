def record_page_time(ts, time, error=False, kb=0):
    """Record the load time for a USER, this is typically across multiple iterations within a user

    :param ts: int Timestamp of request end
    :param time: int elapsed time request took
    :param error: boolean Was this request an error
    :param kb: int Size of request
    """
    print("record_page_time(%f, %f, %r, %i)" % (ts, time, error, kb))


def record_user_start(userid, ts):
    """Record a user thread starting

    :param userid: int user id
    :param ts: int time user/thread was started
    """
    print("record_user_start(%i, %f)" % (userid, ts))


def record_user_stop(userid, ts, time, err=False):
    """Record a user thread stopping

    :param userid: int user id
    :param ts: int ts
    :param time: int elapsed time
    :param err: if this user stopped because of an error
    """
    print("record_user_stop(%s, %f, %f, %r)" % (userid, ts, time, err))


def record_url_page_load(url, ts, time, error=False, kb=0):
    """Record URL load

    :param url: string Naming the request, can be URL or just name
    :param ts: int Timestamp of request end
    :param time: int Elapsed time request took
    :param error: boolean Was this request an error
    :param kb: int size of request
    """
    print("record_url_page_load(%s, %f, %f, %r, %i)" % (url, ts, time, error, kb))


def record_error(error):
    """Record generic error message, not specific to a request or user

    :param error: string Error string
    """
    print("record_error: %s" % error)


def record_download_size(kb):
    """Record download size, not specific to a request
    You can now use @see recordPageTime or @see recordURLPageLoad and include download size

    :param kb: int Size of request
    """
    print("record_download_size(%i)" % kb)


def record_progress(test_num, percent):
    """Record progress of the test (0-100)

    :param test_num: int Test number available
    :param percent: int Should reflect test completeness
    :return:
    """
    print("record_progress(%i, %i)" % (test_num, percent))  # NOTE assuming percent is int