import wandb
import os
import pickle
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI

category_other = ['color_furniture','color_exterior','origin', 'gearbox', 'driver', 'model']
numeric_features = ['year_manufacture','km','num_seat','num_door']
category_features = ['branch','_class','origin','color_exterior','color_furniture','gearbox','driver','model']
FEATURES = numeric_features + category_features

class Input(BaseModel):
    year_manufacture: int
    km: int
    num_seat: int
    num_door: int
    branch: str
    class_: str
    origin: str
    color_exterior: str
    color_furniture: str
    gearbox: str
    driver: str
    model: str
project_name = 'final'
run = wandb.init(project=project_name, job_type='serving')
artifact = run.use_artifact(f'ndtan-udemy/{project_name}/model:product', type='Model')
model_dir = artifact.download()
artifact = run.use_artifact(f'ndtan-udemy/{project_name}/other-func:product', type='Transform')
other_dir = artifact.download()
artifact = run.use_artifact(f'ndtan-udemy/{project_name}/branch-func:product', type='Transform')
branch_dir = artifact.download()
artifact = run.use_artifact(f'ndtan-udemy/{project_name}/class-func:product', type='Transform')
class_dir = artifact.download()
run.finish()

with open(os.path.join(model_dir, 'model.pkl'), 'rb') as file:
    model = pickle.load(file)

with open(os.path.join(branch_dir, 'branch-func.pkl'), 'rb') as file:
    transform_branch = pickle.load(file)

with open(os.path.join(class_dir, 'class-func.pkl'), 'rb') as file:
    transform_class = pickle.load(file)

with open(os.path.join(other_dir, 'other-func.pkl'), 'rb') as file:
    transform_other = pickle.load(file)


api = FastAPI(title="MLOps", version='0.1.0')

@api.post('/api/predict')
def predict(input: Input):
    value = [input.year_manufacture, input.km, input.num_seat, input.num_door,
             input.branch, input.class_, input.origin, input.color_exterior,
             input.color_furniture, input.gearbox, input.driver, input.model]

    df = pd.DataFrame(data=[value], columns=FEATURES)

    df['branch'] = transform_branch.transform(df['branch'])
    df['_class'] = transform_class.transform(df['_class'])
    df[category_other] = transform_other.transform(df[category_other])
    df = df[FEATURES]
    price = model.predict(df)[0]
    return {'price': price}
