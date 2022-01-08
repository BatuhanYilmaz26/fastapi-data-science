import os
from token import OP
import joblib
from typing import List, Optional, Tuple
from fastapi import FastAPI, Depends, status
from joblib import memory
from pydantic import BaseModel
from sklearn.pipeline import Pipeline

# Caching results with Joblib
# If your model takes time to make predictions, it may be interesting to cache the results: 
# if the prediction for a particular input has already been done, it makes sense to return the same result we saved on disk, rather than running the computations again. 
# In this example, we'll learn how to do this with the help of Joblib.

# Joblib provides us with a very convenient and easy-to-use tool to do this, so the implementation is quite straightforward. 
# The main concern will be about whether we should choose standard or async functions to implement the endpoints and dependencies.
# This will allow us to explain some of the technical details of FastAPI in more detail.
# We'll build upon the previous example. (prediction_endpoint.py)

class PredictionInput(BaseModel):
    text: str


class PredictionOutput(BaseModel):
    category: str


# The first thing we must do is initialize a Joblib Memory class, which is the helper for caching functions results.
# Then, we can add a decorator to the functions we want to cache. 
# You can see this in the following example:

memory = joblib.Memory(location="cache.joblib")

@memory.cache(ignore=["model"])
def predict(model: Pipeline, text: str) -> int:
    prediction = model.predict([text])
    return prediction[0]

# When initializing memory, the main argument is location, which is the directory path where Joblib will store the results. 
# Joblib automatically saves cached results on the hard disk.

# Then, you can see that we implemented a predict function that accepts our scikitlearn model, some text input, and then returns the predicted category index.
# This is the same prediction operation we've seen so far. 
# Here, we extracted it from the NewsgroupsModel dependency class because Joblib caching is primarily designed to work with regular functions. 
# Caching class methods is not recommended. 
# As you can see, we simply have to add a @memory.cache decorator on top of this function to enable Joblib caching.
# Whenever this function is called, Joblib will check if it has the result on disk for the same arguments. 
    # If it does, it returns it directly. 
    # Otherwise, it proceeds with the regular function call.
# As you can see, we added an ignore argument to the decorator, which allows us to tell Joblib to not take into account some arguments in the caching mechanism. 
# Here, we excluded the model argument. Joblib cannot dump complex objects, such scikit-learn estimators. 
# This isn't a problem, though: the model is not changing between several predictions, so we don't care about having it cached. 
# If we make improvements to our model and deploy a new one, all we have to do is clear the whole cache so that older predictions are made again with the new model.

# Now, we can tweak the NewsgroupsModel dependency class so that it works with this new predict function. 
# You can see this in the following example:

class NewsgroupsModel:
    model: Optional[Pipeline]
    targets: Optional[List[str]]

    def load_model(self):
        """Loads the model"""
        model_file = os.path.join(os.path.dirname(__file__), "newsgroups_model.joblib")
        loaded_model: Tuple[Pipeline, List[str]] = joblib.load(model_file)
        model, targets = loaded_model
        self.model = model
        self.targets = targets

    def predict(self, input: PredictionInput) -> PredictionOutput:
        """Runs a prediction"""
        if not self.model or not self.targets:
            raise RuntimeError("Model is not loaded")
        prediction = predict(self.model, input.text)
        category = self.targets[prediction]
        return PredictionOutput(category=category)


app = FastAPI()
newgroups_model = NewsgroupsModel()

# In the predict method, we are calling the external predict function instead of doing so directly inside the method, taking care to pass the model and the input text as arguments. 
# All we have to do after is retrieve the corresponding category name and build a PredictionOutput object.

# Finally, we have the REST API endpoints. 
# Here, we added a DELETE/cache route so that we can clear the whole Joblib cache with an HTTP request. 
# This can be seen in the following example:

@app.post("/prediction")
def prediction(
    output: PredictionOutput = Depends(newgroups_model.predict),
) -> PredictionOutput:
    return output


@app.delete("/cache", status_code=status.HTTP_204_NO_CONTENT)
def delete_cache():
    memory.clear()


@app.on_event("startup")
async def startup():
    newgroups_model.load_model()

# The clear method of the memory object removes all the Joblib cache files on the disk.
# Our FastAPI application is now caching prediction results. 
# If you make a request with the same input twice, the second response will show you the cached result. 
# In this example, our model is fast, so you won't notice a difference in terms of execution time; however, this could be interesting with more complex models.

# We can run this application using Uvicorn, as usual:
# $ uvicorn caching:app

# Now, we can try to run some predictions with HTTPie:
# $ http POST http://localhost:8000/prediction text="computer cpu memory ram"