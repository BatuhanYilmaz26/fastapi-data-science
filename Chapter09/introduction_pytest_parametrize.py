import pytest
from Chapter09.introduction import add

# pytest provides powerful tools to help us write tests. 
# Before focusing on FastAPI testing, we'll review two of them: parametrize and fixtures.

# Generating tests with parametrize
# In our previous example(introduction_pytest.py) with the add function, we only tested one addition test, 2 + 3.
# Most of the time, we'll want to check for more cases to ensure our function works in every circumstance. 

# In pytest, a marker is a special decorator that's used to easily pass metadata to the test. 
# Special behaviors can then be implemented, depending on the markers used by the test.
# Here, parametrize allows us to pass several sets of variables that will be passed as arguments to the test function. 
# At runtime, each set will generate a new and independent test. 
# To understand this better, let's look at how to use this marker to generate several tests for our add function:

@pytest.mark.parametrize("a,b,result", [(2, 3, 5), (0, 0, 0), (100, 0, 100), (1, 1, 2)])
def test_add(a, b, result):
    assert add(a, b) == result

# Here, you can see that we simply decorated our test function with the parametrize marker. 
# The basic usage is as follows: 
    # the first argument is a string with the name of each parameter separated by a comma. 
    # Then, the second argument is a list of tuples. 
# Each tuple contains the values of the parameters in order.

# Our test function receives those parameters in arguments, each one named the way you specified previously. 
# Thus, you can use them at will in the test logic. 
# As you can see, the great benefit here is that we only have to write the assert statement once. 
# Besides, it's very quick to add a new test case: we just have to add another tuple to the parametrize marker.

# Now, let's run this test to see what happens by using the following command:
# $ pytest Chapter09/introduction_pytest_parametrize.py

# As you can see, pytest executed four tests instead of one! 
# This means that it generated four independent tests, along with their own sets of parameters. 
# If several tests are failing, we'll be informed, and the output will tell us which set of parameters caused the error.
# To conclude, parametrize is a very convenient way to test different outcomes when it's given a different set of parameters.