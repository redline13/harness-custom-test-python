# Example INI file
# classname = LoadTestingSinglePage
# url = "http://mrc.localhost/"

from load_testing_test import LoadTestingTest, LoadTestingTestException

import record_helpers

# helper functions
import helpers

# to check for a file existence
import os

# to encode into json
import json

# to use sleep() func
import time

# to print out error
import traceback

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


# Single Page Load Testing
class LoadTestingSinglePage(LoadTestingTest):
    def __init__(self, test_num, rand):
        """Constructor

        :param test_num: int Test number
        :param rand: string Random token for test
        """
        # Parameters
        self.__parameters = {
            'get': {},
            'post': {}
        }

        # Call parent constructor
        super(LoadTestingSinglePage, self).__init__(test_num, rand)

    def set_ini_settings(self, ini_settings):
        """Set ini settings

        :param ini_settings: dictionary INI settings
        """
        super(LoadTestingSinglePage, self).set_ini_settings(ini_settings)

        # Check if we should load external resources
        if not helpers.empty(self.__ini_settings, 'load_resources'):
            # TODO: Should we limit which external resources are loaded?
            self.__session.loadable_resource_base_url = 'http'
            self.enable_resource_loading()

        # Set up parameters
        if not helpers.empty(self.__ini_settings, 'parameter_file') and \
                os.path.exists(self.__ini_settings['parameter_file']):
            f = open(self.__ini_settings['[parameter_file]'])
            json_obj = json.dumps(f.read())
            f.close()
            if json_obj:
                if not helpers.empty(json_obj, 'get'):
                    self.__parameters['get'] = json_obj['get']
                if not helpers.empty(json_obj, 'post'):
                    self.__parameters['post'] = {}
                    for parameter in json_obj['post']:
                        self.__parameters['post'][parameter['name']] = parameter['val']

    def start_test(self):
        """ Start the test """
        try:
            # Sleep for ramp up time
            if helpers.isset(self.__ini_settings, 'ramp_up_time_sec') and \
                            self.__ini_settings['ramp_up_time_sec'] > 0 and \
                    helpers.isset(self.__ini_settings, 'num_users'):
                sleep = int(round(self.__test_num / self.__ini_settings['num_users'] *
                                  self.__ini_settings['ramp_up_time_sec']))
                time.sleep(sleep)

            # Load page
            self.load_page()

            # Clean up session file
            self.__session.cleanup()
        except:
            print("Test failed.")

            # Throw exception
            traceback.print_exc()

    def load_page(self):
        """Load page

        :return: LoadTestingPageResponse Page
        """
        # Check for URL
        if helpers.empty(self.__ini_settings, 'url'):
            raise LoadTestingTestException('URL not specified.')

        # Check for number of iterations
        iterations = 1
        if helpers.isset(self.__ini_settings, 'num_iterations'):
            iterations = self.__ini_settings['num_iterations']

        # Iterate
        for i in range(iterations):
            # Build URL
            url = self.__ini_settings['url']
            if not helpers.empty(self.__parameters, 'get'):
                param_str = []
                for tmp in self.__parameters['get']:
                    # TODO: using simple urlencode that doesn't support
                    # multidimensional dictionaries. Testing is required
                    # to make sure it works as expected
                    param_str.append("%s=%s" % (urlencode(tmp['name']),
                                                urlencode(tmp['value'])))
                    del tmp
                    param_str = '&'.join(param_str)

                    question_pos = url.find('?')
                    hash_pos = url.find('#')
                    if question_pos != -1:
                        if hash_pos != -1:
                            url = "%s&%s%s" % (url[0:hash_pos], param_str, url[:hash_pos])
                        else:
                            url = "%s&%s" % (url, param_str)
                    else:
                        if hash_pos != -1:
                            url = "%s?%s%s" % (url[0:hash_pos], param_str, url[:hash_pos])
                        else:
                            url = "%s?%s" % (url, param_str)

            # Should we store output as we test
            store_output = not helpers.empty(self.__ini_settings, 'store_output')

            # Load page
            self.__session.go_to_url(url, self.__parameters['post'], [], store_output)

            # Record progress
            record_helpers.record_progress(self.__test_num, (i + 1) / iterations * 100)
