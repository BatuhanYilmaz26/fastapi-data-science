import numpy as np

# Manipulating arrays with NumPy computation, aggregations, comparisons
# NumPy is all about manipulating large arrays with great performance and controlled memory consumption. 
# Let's say, for example, that we want to compute the double of each element in a large array. 
# In the following example, you can see an implementation of such a function with a standard Python loop:

np.random.seed(0)  # Set the random seed to make examples reproducible

m = np.random.randint(10, size=1000000)  # An array with a million of elements


def standard_double(array):
    output = np.empty(array.size)
    for i in range(array.size):
        output[i] = array[i] * 2
    return 

# We instantiate an array with a million random integers. 
# Then, we have our function building an array with the double of each element. 
# Basically, we first instantiate an empty array of the same size before looping over each element to set the double.
# Let's measure the performance of this function. In Python, there is a standard module, timeit, dedicated to this purpose. 
# We can use it directly from the command line and pass in argument-valid Python statements that we want to measure performance. 
# The following command will measure the performance of standard_double with our big array:
# $ python -m timeit "from Chapter11.compare_operations import m, standard_double; standard_double(m)"
# 1 loop, best of 5: 315 msec per loop

# The results will vary depending on your machine, but the magnitude should be equivalent.
# What timeit does is to repeat your code a certain number of times and measure its execution time. 
# Here, our function took around 300 milliseconds to compute the double of each element in our array. 
# For such simple computations on a modern computer, that's not very impressive.

# Let's compare this with the equivalent operation using NumPy syntax. You can see it in the next sample:

def numpy_double(array):
    return array * 2

# The code is much shorter! NumPy implements the basic arithmetic operations and can apply them to each element of the array. 
# By multiplying the array by a value directly, we implicitly tell NumPy to multiply each element by this value. 
# Let's measure the performance with timeit:
# $ python -m timeit "from Chapter11.compare_operations import m, numpy_double; numpy_double(m)"
# 500 loops, best of 5: 667 usec per loop

# Here, the best loop achieved the computation in 600 microseconds! 
# That's almost a thousand times faster than the previous function! How can we explain such a variation? 
# In a standard loop, Python, because of its dynamic nature, has to check for the type of value at each iteration to apply the right function for this type, which adds significant overhead. 
# With NumPy, the operation is deferred to an optimized and compiled loop where types are known ahead of time, which saves a lot of useless checks.