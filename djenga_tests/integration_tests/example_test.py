from djenga.test import IntegrationTest


class ExampleTest(IntegrationTest):
    def test_add(self):
        x = 1 + 1
        self.assert_equal(x, 2)
        x += 5
        self.assert_equal(7, x)
