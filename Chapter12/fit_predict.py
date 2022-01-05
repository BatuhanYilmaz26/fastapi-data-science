from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

digits = load_digits()

data = digits.data
targets = digits.target

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, targets, test_size=0.3, random_state=42)

# Train the model
model = GaussianNB()
model.fit(X_train, y_train)

# Run prediction with the testing set
y_pred = model.predict(X_test)

# Compute the accuracy
accuracy = round(accuracy_score(y_test, y_pred), 2)
print(accuracy)