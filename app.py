from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
import pickle
import pandas as pd
from Schema.user_input_validation import UserINPUT
from Model.predict import predict_output, model, MODEL_VERSION

app = FastAPI()

# Human Readable
@app.get('/')
def home():
    return {"Message" : "Insurance prediction API"}

# Machine Readable for platforms like Qubernetes as they require a health check for proper deployment
@app.get('/health')
def health():
    return {'Status' : 'OK',
    'Version' : MODEL_VERSION,
    'Model_Loaded' : model is True}

@app.post('/predict')
def predict_premium(data: UserINPUT):
    input_dict = {
        'bmi' : data.bmi,
        'age_group' : data.age_group,
        'Life_style_risk' : data.lifestyle_risk,
        'city_tier' : data.city_tier,
        'income_lpa' : data.income_lpa,
        'occupation' : data.occupation
    }
    try:
        prediction = predict_output(input_dict)

        return JSONResponse(status_code=200, content={'predicted_category': prediction})
    except Exception as e:
        return JSONResponse(status_code=500, content = str(e))