#NOTE: untested as for now

# to parse ini config
from php.php import Php # TODO: ini_parser doesn't work without sections therefore is not a good choice; rewrite using python's configparser.

# to set fatal handler function
import sys

# to call a function on exit
import atexit

@atexit.register
def exit_func():
    print("Completed test")


# TODO: docstringify
# /**
#  * used to capture to look for caught errors on exit.
#  * @internal
#  */
def fatal_handler(type, value, tb):
    print("record_fatal_error: %s" % value)


# inner on error function
def fatal_handler(type, value, tb):
    tb_list = traceback.extract_tb(tb)
    print("Python fatal error in %s[%s]: %s" % (os.path.basename(tb_list[0][0]), \
                                                tb_list[0][1], value))


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


# set function to execute on fatal error
sys.excepthook = fatal_handler

try:
    # Parse ini file
    try:
        config = Php.parse_ini_file('loadtest.ini')
    except:
        pass

    # Update running count
    print("Load_agent_running")

    # Register shutdown function
    sys.excepthook = inner_fatal_handler

    # Get classname
    if sys.argv[1]:
        classname = sys.argv[1]
    elif helpers.empty(config, 'classname'):
        raise RuntimeError('Classname not specified.')
    else:
        classname = config['classname']

    # Set up object
    module_ = __import__(classname)
    class_ = getattr(module_, classname)
    test = class_(1, None)
    try:
        set_ini_settings = getattr(test, "set_ini_settings")
        set_ini_settings(config)
    except:
        pass

    # Check for delay
    if helpers.isset(config, 'min_delay_ms') && helpers.isset("max_delay_ms"):
        try:
            set_delay = getattr(test, "set_delay")
            set_delay(config['min_delay_ms'], config['max_delay_ms'])
        except:
            pass

    # Start test
        try:
            start_test = getattr(test, "start_test")
            start_test()
        except:
            raise RuntimeError('Invalid test script.')

except Exception as e:
    print("record_exception: %s" % str(e))
