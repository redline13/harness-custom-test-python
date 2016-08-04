from load_testing_session import LoadTestingSession

# to use helper functions
import helpers


class LoadTestingTestException(Exception):
    """ Load Testing Test Exception """
    pass


class LoadTestingTest(object):
    def __init__(self, test_num, rand, resource_url=None):
        """Constructor

        :param test_num: int Test Number
        :param rand: string Random token for test
        :param resource_url: string Optional URL specifying host that resources will
        be loaded for. The hostname is grabbed from this URL.
        """

        # Verbose mode
        self.__verbose = False

        # Ini settings
        self.__ini_settings = {}

        # LoadTestingSession Access to object to invoke requests to pages and wrap CURL.
        self.session = LoadTestingSession(test_num, rand)

        # Save test number
        self.__test_num = test_num

        # Load resource only from base url
        if resource_url and helpers.is_absolute_base(resource_url):
            self.session.loadable_resource_base_url = helpers.get_absolute_base(resource_url)

    def enable_resource_loading(self):
        """ Enable resource loading """
        self.session.enable_resource_loading()

    def disable_resource_loading(self):
        """ Disable resource loading """
        self.session.disable_resource_loading()

    def set_delay(self, min_delay_ms, max_delay_ms):
        """Set delay between page loads

        :param min_delay_ms: int Minimum delay in ms
        :param max_delay_ms: int Maximum delay in ms
        """
        self.session.set_delay(min_delay_ms, max_delay_ms)

    def get_delay(self):
        """Gets most recently used delay

        :return: int Most recent delay used
        """
        return self.session.get_delay()

    def set_ini_settings(self, ini_settings):
        """Set ini settings

        :param ini_settings: dictionary INI settings
        """
        self.__ini_settings = ini_settings

    def get_ini_settings(self):
        """Get the iniSettings (dictionary)

        :return: dictionary Settings for test
        """
        return self.__ini_settings

    def get_session(self):
        """Get the session object, which wraps CURL for simple tests

        :return: LoadTestingSession Session object
        """
        return self.session

    def verbose(self):
        """ Verbose """
        self.__verbose = True
        self.session.verbose()

    def non_verbose(self):
        """ Non-verbose """
        self.__verbose = False
        self.session.non_verbose()

    def start_test(self):
        """Start the test
        This method throws the Exception! In order to start the test it has to be overrided with
        the actual implementation (behaviour imitates abstract method in the more pythonic way)
        """
        raise NotImplementedError()
