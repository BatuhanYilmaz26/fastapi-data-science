# Introduction to unit testing with pytest
# Writing unit tests is an essential task in software development to deliver high-quality software. 
# To help us be productive and efficient, lot of libraries exist that provide tools and shortcuts dedicated to testing. 
# In the Python standard library, a module exists for unit testing called unittest. 
# Even though it's quite common in Python code bases, many Python developers tend to prefer pytest, which provides a more lightweight syntax and powerful tools for advanced use cases.
# In the following examples, we'll write a unit test for a function called add, both with unittest and pytest, so that you can see how they compare on a basic use case. 

def add (a: int, b: int) -> int:
    return a + b

# Now, let's implement a test that checks that 2 + 3 is indeed equal to 5 with unittest: --> introduction_unittest.py