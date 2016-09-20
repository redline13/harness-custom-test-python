# internal helper functions
import helpers

# to extract traceback, for fatal errors.
import traceback

# to set fatal handler function
import sys

# to get the basename of a file
import os

# to call a function on exit
import atexit

# to remove temp folder
import shutil

# to parse INI config
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

# to mimic file-like behavior
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

@atexit.register
def exit_func():
    """ Removing temp 'cookies' folder that is created in load_testing_session.py and exiting """
    if os.path.exists('cookies'):
        shutil.rmtree('cookies')
    print("Completed test")

def fatal_handler(type, value, tb):
    """Used to capture to look for caught errors on exit

    :param type: string Type of the error
    :param value: string Value of the error (message)
    :param tb: Traceback object
    """
    print("record_fatal_error: %s" % value)

# Something goes bad internally.
def inner_fatal_handler(type, value, tb):
    """ Inner on error function """
    tb_list = traceback.extract_tb(tb)
    if type is not KeyboardInterrupt:
        print("Python fatal error in %s[%s]: %s" % (os.path.basename(tb_list[0][0]),
                                                    tb_list[0][1], value))

# set function to execute on fatal error
sys.excepthook = fatal_handler

try:
    # Parse ini file
    config = None
    try:
        raw_config = "[s]\n"
        with open('loadtest.ini', 'r') as f:
            raw_config += f.read()
        config = ConfigParser()
        config.readfp(StringIO(raw_config))
        config = dict(config.items('s'))
    except:
        pass

    # Update running count
    print("Load_agent_running")

    # Register shutdown function
    sys.excepthook = inner_fatal_handler

    # Get classFilename
    cn = None
    try:
        cn = sys.argv[1]
    except IndexError:
        pass
    if cn:
        classFilename = sys.argv[1]
    elif not config:
        raise RuntimeError('No Configuration Available')
    elif helpers.empty(config, 'classfilename'):
        raise RuntimeError('classfilename not specified.')
    else:
        classFilename = config['classfilename']

    # Set up object
    module_ = __import__(classFilename)
    from load_testing_test import LoadTestingTest
    subClasses = LoadTestingTest.__subclasses__()
    if len(subClasses) == 1:
        class_ = subClasses[0]
    else:
        raise Exception("Unknown Load Class")
    test = class_(1, 1)

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
    except Exception as e:
        if e is not KeyboardInterrupt:
            raise e

except Exception as e:
    print("record_exception: %s" % str(e))
