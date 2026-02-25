import pickle
import pandas as pd

with open('Model/model.pkl', 'rb') as f:
    model  = pickle.load(f)

MODEL_VERSION = '1.22.1'

def predict_output(input_data : dict):
    input_df = pd.DataFrame([input_data])

    output = model.predict(input_df)[0]

    return output