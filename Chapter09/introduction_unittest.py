import unittest
from Chapter09.introduction import add


class TestChapter09Introduction(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

# As you can see, unittest expects us to define a class inheriting from TestCase.
# Then, each test lives in its own method. To assert that two values are equal, we must use the assertEqual method.
# To run this test, we can call the unittest module from the command line and pass it through the dotted path to our test module:
# $ python -m unittest Chapter09.introduction_unittest

# In the output, each successful test is represented by a dot. 
# If one or several tests are not successful, you will get a detailed error report for each, highlighting the failing assertion.
# You can try it by changing the assertion in the test.
# Now, let's write the same test with pytest: --> introduction_pytest.py