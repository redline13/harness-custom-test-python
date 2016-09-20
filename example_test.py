from load_testing_test import LoadTestingTest
import record_helpers
import time
import random


class ExampleTest(LoadTestingTest):

    def __init__(self, test_num, rand):
        """Constructor

        :param test_num: int Test number
        :param rand: string Random token for test
        """
        self.tester = test_num

        # Call parent constructor
        super(ExampleTest, self).__init__(test_num, rand)

    def start_test(self):
        """ Start test """

        # Example getting information from Config Dict
        config = self.get_ini_settings()
        iterations = 5
        if config.has_key( 'iterations' ):
            iterations = int(config.get( 'iterations', 1 ))

        start_user_time = time.time()

        for x in range(1, iterations+1):
            start_time = time.time()
            rand_time = random.randint(2, 5)
            time.sleep(rand_time)
            diff = time.time() - start_time
            record_helpers.record_load( x, start_time, diff)

        end_user_elapsed = time.time() - start_user_time
        record_helpers.record_load( "Overall", start_user_time, end_user_elapsed)

        return True
