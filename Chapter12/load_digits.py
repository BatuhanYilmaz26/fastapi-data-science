from numpy.lib.npyio import load
from sklearn.datasets import load_digits

digits = load_digits()

data = digits.data
targets = digits.target

print(data[5].reshape(8, 8)) # Fifth handwritten digit 8 x 8 matrix
print(targets[5]) # Label of the fifth handwritten digit