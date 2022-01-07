import os
import joblib
from typing import List, Optional, Tuple
from fastapi import FastAPI, Depends
from joblib.numpy_pickle import load
from pydantic import BaseModel
from sklearn.pipeline import Pipeline

# Implementing an efficient prediction endpoint
# Now that we have a way to save and load our machine learning models, it's time to use them in a FastAPI project.
# The main part of the implementation is the class dependency, which will take care of loading the model and making predictions.
# Our example will be based on the newgroups model we dumped in the previous section. 
# We'll start by showing you how to implement the class dependency, which will take care of loading and making predictions:

class PredictionInput(BaseModel):
    text: str


class PredictionOutput(BaseModel):
    category: str


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
    
    async def predict(self, input: PredictionInput) -> PredictionOutput:
        """Runs a prediction"""
        if not self.model or not self.targets:
            raise RuntimeError("Model is not laoded")
        prediction = self.model.predict([input.text])
        category = self.targets[prediction[0]]
        return PredictionOutput(category=category)

# First, we start by defining two Pydantic models: PredictionInput and PredictionOutput. 
# In a pure FastAPI philosophy, they will help us validate the request payload and return a structured JSON response. 
# Here, as input, we simply expect a text property containing the text we want to classify; in terms of the output, we expect a category property containing the predicted category.

# The most interesting part of this extract is the NewsgroupsModel class. 
# It implements two methods: load_model and predict. 

# The load_model method loads the model using Joblib, as we saw in the previous section, and stores the model and the targets in class properties. 
# Hence, they will be available for use by the predict method.

# On the other hand, the predict method will be injected into the path operation function. 
# As you can see, it directly accepts a PredictionInput that will be injected by FastAPI. 
# Inside this method, we are making a prediction, as we usually do with scikit-learn. 
# We return a PredictionOutput object with the category we predicted.


app = FastAPI()
newgroups_model = NewsgroupsModel()


@app.post("/prediction")
async def prediction(
    output: PredictionOutput = Depends(newgroups_model.predict),
) -> PredictionOutput:
    return output


@app.on_event("startup")
async def startup():
    newgroups_model.load_model()

# We are creating an instance of NewsgroupsModel so that we can inject it into our path operation function. 
# Moreover, we are implementing a startup event handler to call load_model. 
# This way, we are making sure that the model is loaded during application startup and is ready to use.

# The prediction endpoint is quite straightforward: as you can see, we directly depend on the predict method, which will take care of injecting the payload and validating it.
# We only have to return the output.

# That's it! Once again, FastAPI makes our life very easy by allowing us to write very simple and readable code, even for complex tasks. 
# We can run this application using Uvicorn, as usual:
# $ uvicorn prediction_endpoint:app

# Now, we can try to run some predictions with HTTPie:
# $ http POST http://localhost:8000/prediction text="computer cpu memory ram"

# Our machine learning classifier is alive! 
# To push this further, in the next example we'll see how we can implement a simple caching mechanism using Joblib. --> caching.py