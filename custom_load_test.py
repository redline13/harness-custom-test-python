from load_testing_test import LoadTestingTest


class CustomLoadTest(LoadTestingTest):
    """ Custom load test template to test out arbitrary functionality """

    def __init__(self, test_num, rand):
        """Constructor

        :param test_num: int Test number
        :param rand: string Random token for test
        """
        # Call parent constructor
        super(CustomLoadTest, self).__init__(test_num, rand)

    def start_test(self):
        """ Start test """
        url = 'http://www.echoecho.com/htmlforms11.htm'
        page = self.session.go_to_url(url=url, save_data=True)
