from Chapter09.introduction import add

def test_add():
    assert add(2, 3) == 5

# As you can see, it's much shorter! 
# Indeed, with pytest, you don't necessarily have to define a class: a simple function is enough. 
# The only constraint to making it work is that the function name has to start with test_. 
# This way, pytest can automatically discover the test functions. 
# Secondly, it relies on the built-in assert statement instead of specific methods, allowing you to write comparisons more naturally.
# To run this test, we must simply call the pytest executable with the path to our test file:
# $ pytest Chapter09/introduction_pytest.py

# Once again, the output represents each successful test with a dot. 
# Of course, if you change the test to make it fail, you'll get a detailed error for the failing assertion.
# It's worth noting that if you run pytest without any arguments, it'll automatically discover all the test files living in your folder, as long as their name starts with test_.
# Here, we made a small comparison between unittest and pytest. 
# For the rest of this chapter, we'll stick with pytest, which should give you a more productive experience while writing tests.
