from load_testing_test import LoadTestingTest
import time
import random


class SimpleLoadTest(LoadTestingTest):
    """ Single Page Load Testing """

    def __init__(self, test_num, rand):
        """Constructor

        :param test_num: int Test number
        :param rand: string Random token for test
        """
        # Call parent constructor
        super(SimpleLoadTest, self).__init__(test_num, rand)

    def start_test(self):
        """ Start the test and load it's resources"""
        try:
            ## Enable Resource Loading 
            self.enable_resource_loading()
            self.session.loadable_resource_base_url = 'http'
            # Load page
            page = self.load_page()

            # Clean up session file
            self.session.cleanup()
        except Exception as e:
            print("Test failed.")
            raise e

    def load_page(self):
        """Load page

        :return: LoadTestingPageResponse page
        """
        # Sleep between 0.000001 and 10 seconds
        time.sleep(random.uniform(0.000001, 10))

        # Load page
        page = self.session.go_to_url('https://www.yahoo.com')

        return page
