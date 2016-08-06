from load_testing_test import LoadTestingTest

class CustomLoadTest(LoadTestingTest):

    def __init__(self, test_num, rand):
        # Call parent constructor
        super(CustomLoadTest, self).__init__(test_num, rand)

    def start_test(self):
        url = 'http://keddr.com'
        self.session.verbose()
        self.session.enable_resource_loading()
        self.session.loadable_resource_base_url = 'http://keddr.com'
        page = self.session.go_to_url(url=url, save_data=True)
        self.session.non_verbose()
        page = self.session.go_to_url(url=url, save_data=True)
