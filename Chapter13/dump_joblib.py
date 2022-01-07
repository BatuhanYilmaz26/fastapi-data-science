import joblib
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Persisting a trained model with Joblib
# In the previous chapter, you learned how to train an estimator with scikit-learn. 
# When building such models, you'll likely obtain a rather complex Python script to load your training data, pre-process it, and train your model with the best set of parameters. 
# However, when deploying your model in a web application, such as FastAPI, you don't want to repeat this script and run all those operations when the server is starting. 
# Instead, you need a ready-to-use representation of your trained model that you can just load and use.
# This is what Joblib does. 
# This library aims to provide tools for efficiently saving Python objects to disk, such as large arrays of data or function results: this operation is generally called dumping. 
# Joblib is already a dependency of scikit-learn, so we don't even need to install it. 
# scikit-learn uses it internally to load the bundled toy datasets.
# As we'll see, dumping a trained model involves just one line of code with Joblib.

# Dumping a trained model
# In this example, we're using the newsgroups example we saw in the Chaining pre-processors and estimators with pipelines section of Chapter 12. 
# As a reminder, we load four categories of the 20 newsgroups dataset and build a model to automatically categorize news articles into those categories. 
# Once we've done this, we dump the model into a file called newsgroups_model.joblib:

# Load some categories of newsgroups dataset
categories = [
    "soc.religion.christian",
    "talk.religion.misc",
    "comp.sys.mac.hardware",
    "sci.crypt",
]
newsgroups_training = fetch_20newsgroups(
    subset="train", categories=categories, random_state=0
)
newsgroups_testing = fetch_20newsgroups(
    subset="test", categories=categories, random_state=0
)

# Make the pipeline
model = make_pipeline(
    TfidfVectorizer(),
    MultinomialNB(),
)

model.fit(newsgroups_training.data, newsgroups_training.target)

# Serialize the model and the target names
model_file = "newsgroups_model.joblib"
model_targets_tuple = (model, newsgroups_training.target_names)
joblib.dump(model_targets_tuple, model_file)

# As you can see, Joblib exposes a function called dump, which simply expects two arguments: the Python object to save and the path of the file.

# Notice that we don't dump the model variable alone: instead, we wrap it in a tuple, along with the name of the categories, target_names. 
# This allows us to retrieve the actual name of the category after the prediction has been made, without us having to reload the training dataset.

# If you run this script, you'll see that the newsgroups_model.joblib file was created:
# $ python Chapter13/dump_joblib.py
# $ ls -lh *.joblib

# Notice that this file is rather large: it's more than 3 MB! 
# It stores all the probabilities of each word in each category, as computed by the Multinomial Naive Bayes model.
# That's all we need to do. 
# This file now contains a static representation of our Python model, which will be easy to store, share, and load. 
# In the next example, we'll learn how to load it and check that we can run predictions on it. --> load_joblib.py