from load_testing_test import LoadTestingTest
import record_helpers
import time
import random


class ExampleTest(LoadTestingTest):

    def start_test(self):
        """ Start test """

        # Example getting information from Config Dict
        config = self.get_ini_settings()
        iterations = 1
        if config.has_key( 'iterations' ):
            iterations = int(config.get( 'iterations', 1 ))

        start_user_time = time.time()

        for x in range(1, iterations):
            start_time = time.time()
            time.sleep(random.randint(2, 5))
            diff = time.time() - start_time
            record_helpers.record_url_page_load(x, start_time, diff)

        end_user_elapsed = time.time() - start_user_time
        record_helpers.record_page_time(start_user_time, end_user_elapsed)

        return True
