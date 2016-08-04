# helper functions
import helpers

# to extract traceback
import traceback

# to set fatal handler function
import sys

# to get the basename of a file
import os

# to call a function on exit
import atexit


@atexit.register
def exit_func():
    print("Completed test")


def fatal_handler(type, value, tb):
    """Used to capture to look for caught errors on exit

    :param type: string Type of the error
    :param value: string Value of the error (message)
    :param tb: Traceback object
    """
    print("record_fatal_error: %s" % value)


def inner_fatal_handler(type, value, tb):
    """ Inner on error function """
    tb_list = traceback.extract_tb(tb)
    print("Python fatal error in %s[%s]: %s" % (os.path.basename(tb_list[0][0]),
                                                tb_list[0][1], value))


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


# set function to execute on fatal error
sys.excepthook = fatal_handler

try:
    # ----------------- NOT WORKING PART -----------------
    #    # Parse ini file
    #    try:
    #        config = Php.parse_ini_file('loadtest.ini')
    #    except:
    #        pass
    # --------------- NOT WORKING PART END ----------------

    # imitating imported config
    config = {"classname": "ExampleTest"}

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
    if helpers.isset(config, 'min_delay_ms') and helpers.isset(config, "max_delay_ms"):
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
