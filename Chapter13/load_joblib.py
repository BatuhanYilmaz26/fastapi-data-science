import os
import joblib
from typing import List, Tuple
from sklearn.pipeline import Pipeline

# Loading a dumped model
# Now that we have our dumped model file, let's learn how to load it again using Joblib and check that everything is working. 
# In the following example, we're loading the Joblib dump present in the Chapter13 directory and running a prediction:

# Load the model
model_file = os.path.join(os.path.dirname(__file__), "newsgroups_model.joblib")
loaded_model: Tuple[Pipeline, List[str]] = joblib.load(model_file)
model, targets = loaded_model

# Run a prediction
p = model.predict(["computer cpu memory ram"])
print(targets[p[0]])

# All we need to do here is call the load function from Joblib and pass it a valid path to a dump file. 
# The result of this function is the very same Python object we dumped. 
# Here, it's a tuple composed of the scikit-learn estimator and a list of categories.
# Notice that we added some type hints: while not necessary, it helps mypy or your IDE identify the nature of the objects you loaded and benefit from type-checking and auto-completion.
# Finally, we ran a prediction on the model: it's a true scikit-learn estimator, with all the necessary training parameters.

# That's it! As you've seen, Joblib is straightforward to use. 
# Nevertheless, it's an essential tool for exporting your scikit-learn models and being able to use them in external services without repeating the training phase. 
# Now, we can use those dump files in FastAPI projects.