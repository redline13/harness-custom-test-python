#NOTE: untested as for now

# Example INI file
# classname = LoadTestingSinglePage
# url = "http://mrc.localhost/"

import load_testing_test

# helper functions
import helpers

# to check for a file existance
import os

# to encode into json
import json

# to use sleep() func
import time

# to print out error
import traceback

# Single Page Load Testing
class LoadTestingSinglePage(LoadTestingTest):

    # TODO: docstringify
    # /**
	#  * Constructor
	#  * @param int $testNum Test number
	#  * @param string $rand Random token for test
	#  */
    def __init__(test_num, rand):

        # Parameters
        self.__parameters = {
            'get': [], # NOTE: list or map?
            'post': [] # NOTE: list or map?
        }

        # Call parent constructor
        super(LoadTestingSinglePage, self).__init__(test_num, rand)


    # TODO: docstringify
	# /**
	#  * Set ini settings
	#  * @param array $iniSettings INI settings
	#  */
    def set_ini_settings(ini_settings):
        super(LoadTestingSinglePage, self).set_ini_settings(ini_settings)

        # Check if we should load external resources
        if not helpers.empty(self.__ini_settings['load_resources']):
            # TODO: Should we limit which external resources are loaded?
            self.__session.loadable_resource_base_url = 'http'
            self.enable_resource_loading()

        # Set up parameters
        if not helpers.empty(self.__ini_settings['parameter_file']) && \
                        os.path.exists(self.__ini_settings['parameter_file']):
            f = open(self.__ini_settings['[parameter_file]'])
            json_obj = json.dumps(f.read())
            f.close()
            if json_obj:
                if not helpers.empty(json_obj, 'get'):
                    self.__parameters['get'] = json_obj['get']
                if not helpers.empty(json_obj, 'post'):
                    self.__parameters['post'] = {}
                    for parameter in json['post']:
                        self.__parameters['post'][parameter['name']] = parameter['val']


    # TODO: docstringify
    # /**
	#  * Start the test
	#  * @throws LoadTestingTestException
	#  */
    def start_test():
        try:
            # Sleep for ramp up time
            if helpers.isset(self.__ini_settings, 'ramp_up_time_sec') && \
                    self.__ini_settings['ramp_up_time_sec'] > 0 && \
                    helpers.isset(self.__ini_settings, 'num_users'):
                sleep = int(round(self.__test_num/self.__ini_settings['num_users']* \
                        self.__ini_settings['ramp_up_time_sec']))
                time.sleep(sleep)

            # Load page
            self.load_page()

            # Clean up session file
            self.session.cleanup()
        except:
            print("Test failed.")

            # Throw exception
            traceback.print_exc()


    # TODO: docstringify
    # /**
	#  * Load page
	#  * @return LoadTestingPageResponse Page
	#  * @throws LoadTestingTestException
	#  */
    def load_page():
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
                for ### pointer troubles
