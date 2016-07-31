#NOTE: untested as for now

# to register atexit function
import atexit

# to parse ini config
from php.php import Php

# to get the last stacktrace

# TODO: docstringify
# /**
#  * used to capture to look for caught errors on exit.
#  * @internal
#  */
@atexit.register
def fatal_handler():
    error_type = getattr(sys, 'last_type', None)
    if error_type: # NOTE: not checking for an error type (python has no warnings)
        print("record_fatal_error: %s" % sys.last_value) # TODO: REWRITE USING EXC_INFO()


def inner_fatal_handler():
    error_type = getattr(sys, 'last_type', None)
    if error_type:
        print('Python Fatal Error In ') # NOTE: INFINISHED
        # TODO: REWRITE USING EXC_INFO()


# TODO: docstringify
# /**
#  * Record the load time for a USER, this is typically across multiple iterations within a user.
#  * @param int $ts timestamp of request end
#  * @param int $time elapsed time request took
#  * @param boolean $error was this request an error
#  * @param int $kb size of request
#  */
def record_page_time(ts, time, error = False, kb = 0):
    print("record_page_time(%f, %f, %r, %i)" % (ts, time, error, kb))


# TODO: docstringify
# /**
#  * Record a user thread starting.
#  * @param int $userid
#  * @param int $ts time user/thread was strarted
#  */
def record_user_start(userid, ts):
    print("record_user_start(%i, %f)" % (userid, ts))


# TODO: docstringify
# /**
#  * Record a user thread stopping
#  * @param int $userid
#  * @param int $ts
#  * @param int $time elapsed time
#  * @param boolean $err if this user stopped because of an error.
#  */
def record_user_stop(userid, ts, time, err = False):
    print("record_user_stop(%s, %f, %f, %r)" % (userid, ts, time, err))


# TODO: docstringify
# /**
#  * Record URL load
#  * @param string $url Naming the request, can be URL or just NAME
#  * @param int $ts timestamp of request end
#  * @param int $time elapsed time request took
#  * @param boolean $error was this request an error
#  * @param int $kb size of request
#  */
def record_url_page_load(url, ts, time, error = False, kb = 0):
    print("record_url_page_load(%s, %f, %f, %r, %i)" % (url, ts, time, error, kb))


# TODO: docstringify
# /**
#  * Record generic error message, not specific to a request or user.
#  * @param String $error error string
#  */
def record_error(error):
    print("record_error: %s" % error)


# TODO: docstringify
# /**
#  * Record download size, not specific to a request.
#  * You can now use @see recordPageTime or @see recordURLPageLoad and include download size.
#  */
def record_download_size(kb):
    print("record_download_size(%i)" % kb)


# TODO: docstringify
# /**
#  * Record progress of the test (0-100)
#  * @param int $testNum Test Number available $this->testNum
#  * @param int $percent should reflect test completeness.
#  */
def record_progress(test_num, percent):
    print("record_progress(%i, %i)" % (test_num, percent)) # NOTE assuming percent is int


try:
    # Parse ini file
    config = Php.parse_ini_file('loadtest.ini')

    # Update running count
    print("Load_agent_running")

    # Register shutdown function
    atexit.register(inner_fatal_handler)
