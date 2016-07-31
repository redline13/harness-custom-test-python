#NOTE: untested as for now

import load_testing_session

# to add the support for an abstract class definition
from abs import ABCMeta, abstractmethod

# to match with PCRE
import re

# to use helper functions
import helpers

# Load Testing Test Exception
class LoadTestingTestException(Exception):
    pass

class LoadTestingTest:
    __metaclass__ = ABCMeta

    # TODO: docstringify
    # /**
	#  * Constructor
	#  * @param int $testNum Test Number
	#  * @param string $rand Random token for test
	#  * @param string $resourceUrl Optional URL specifying host that resources will
	#  * 	be loaded for.  The hostname is grabbed from this URL.
	#  */
    def __init__(self, test_num, rand, resource_url = None):

        # Verbose mode
        self.__verbose = False

        # Ini settings
        self.__ini_settings = {}

        # TODO: docstringify
        # /** @var LoadTestingSession Access to object to invoke requests to pages and wrap CURL. */
        self.__session = LoadTestingSession(test_num, rand)

        # Save test number
        self.__test_num = test_num

        # Load resourse only from base url
        if resource_url && helpers.is_absolute_base(resource_url):
            self.__session.loadable_resource_base_url = helpers.get_absolute_base(resource_url)


    # Enable resource loading
    def enable_resource_loading(self):
        self.__session.enable_resource_loading()


    # Disable resource loading
    def disable_resource_loading():
        self.__session.disable_resource_loading()


    # TODO: docstringify
    # /**
	#  * Set delay between page loads
	#  * @param int $minDelayMs Minimum delay in ms
	#  * @param int $maxDelayMs Maximum delay in ms
	#  */
    def set_delay(min_delay_ms, max_delay_ms):
        self.__session.set_delay(min_delay_ms, max_delay_ms)


    # TODO: docstringify
    # /**
	#  * Gets most recently used delay.
	#  * @return int
	#  */
    def get_delay():
        return self.__session.get_delay()


    # TODO: docstringify
    # /**
	#  * Set ini settings
	#  * @param array $iniSettings INI settings
	#  */
    def set_ini_settings(ini_settings):
        self.__ini_settings = ini_settings


    # TODO: docstringify
    # /**
	#  * Get the iniSettings (hashmap)
	#  * @return HashMap Settings for test
	#  */
    def get_ini_settings():
        return self.__ini_settings


    # TODO: docstringify
    # /**
	#  * Get the sesssion object, which wraps CURL for simple tests.
	#  * @return LoadTestingSession Session object.
	#  */
    def get_session():
        return self.__session


    # Verbose
    def verbose():
        self.__verbose = True
        self.__session.verbose()


    # Non-verbose
    def non_verbose():
        self.__verbose = False
        self.__session.non_verbose()


    # Start the test
    @abstractmethod
    def start_test():
        return
