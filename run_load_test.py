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


# set function to execute on fatal error
# sys.excepthook = fatal_handler

#try:
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
# sys.excepthook = inner_fatal_handler

# Get classname
cn = None
try:
    cn = sys.argv[1]
except IndexError:
    pass
if cn:
    classname = sys.argv[1]
elif helpers.empty(config, 'classname'):
    raise RuntimeError('Classname not specified.')
else:
    classname = config['classname']

# Set up object
modulename = helpers.un_camel(classname)
module_ = __import__(modulename)
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
#try:
start_test = getattr(test, "start_test")
start_test()
#except:
#    raise RuntimeError('Invalid test script.')

#except Exception as e:
    #print("record_exception: %s" % str(e))
