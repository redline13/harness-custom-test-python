from load_testing_test import LoadTestingTest
import record_helpers
import time
import random


class ExampleTest(LoadTestingTest):

    def start_test(self):
        start_user_time = time.time()

        for x in range(1, 101):
            start_time = time.time()
            time.sleep(random.randint(2, 5))
            diff = time.time() - start_time
            record_helpers.record_url_page_load(x, start_time, diff)

        end_user_elapsed = time.time() - start_user_time
        record_helpers.record_page_time(start_user_time, end_user_elapsed)

        return True
