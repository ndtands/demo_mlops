import pandas as pd
import wandb

import category_encoders as ce
from scipy import stats
import numpy as np
import pickle


CONFIG_DATA ={
    "numeric":{
        "year_manufacture":{
            "lower_limit": 2007,
            "upper_limit":float('inf')
        },
        "km":{
            "lower_limit": 0,
            "upper_limit":1e9
        },
        "num_seat": {
            "lower_limit": 0,
            "upper_limit":30
        },
        "num_door": {
            "lower_limit": 0,
            "upper_limit":30
        }
    },
    "category": {
        "origin": ['domestic', 'imported'],
        "driver": ['FWD', 'RWD', '4WD', 'AWD'],
        "model": ['Sedan', 'Minivan', 'Truck', 'Cabriolet', 'Hatchback', 'Crossover',
                    'Pickup', 'Coupe'],
        "gearbox": ['automatic', 'manual'],
    }
}

category_other = ['color_furniture','color_exterior','origin', 'gearbox', 'driver', 'model']

numeric_features = ['year_manufacture','price','km','num_seat','num_door']
category_features = ['branch','_class','origin','color_exterior','color_furniture','gearbox','driver','model']
FEATURES = numeric_features + category_features


def save_pkl(data, path):
    output = open(path, 'wb')
    pickle.dump(data, output)
    output.close()

def load_pkl(path):
    pkl_file = open(path, 'rb')
    return pickle.load(pkl_file)


def detect_outline(df: pd.DataFrame, feature: str, lower_limit: float = 0,
                   upper_limit: float = float('inf')) -> pd.DataFrame:
    """
    Remove outline of features
    """
    return df[(df[feature] < upper_limit) & (df[feature] > lower_limit)]


def filter_numeric_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outline for feature numeric
    """
    df = detect_outline(df=df, feature='year_manufacture', lower_limit=CONFIG_DATA['numeric']['year_manufacture']['lower_limit'])
    df = detect_outline(df=df, feature='km', upper_limit=CONFIG_DATA['numeric']['km']['upper_limit'])
    df = detect_outline(df=df, feature='num_seat', upper_limit=CONFIG_DATA['numeric']['num_seat']['upper_limit'])
    df = detect_outline(df=df, feature='num_door', upper_limit=CONFIG_DATA['numeric']['num_door']['upper_limit'])
    return df


def filter_category_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outline for feature category
    """
    df = df.loc[df.origin.apply(lambda x: x in CONFIG_DATA['category']['origin'])]
    df = df.loc[df.driver.apply(lambda x: x in CONFIG_DATA['category']['driver'])]
    df = df.loc[df.model.apply(lambda x: x in CONFIG_DATA['category']['model'])]
    df = df.loc[df.gearbox.apply(lambda x: x in CONFIG_DATA['category']['gearbox'])]
    return df


def filter_outline_target(df: pd.DataFrame, z_score: float = 2.8) -> pd.DataFrame:
    df = df[(np.abs(stats.zscore(df.price)) < z_score)]
    return df


class Transform:
    def __init__(self, df_train, df_test, df_val) -> None:
        self.df_train = df_train
        self.df_test = df_test
        self.df_val = df_val

        # init encoder
        self.encoder_branch = ce.JamesSteinEncoder()
        self.encoder_class = ce.JamesSteinEncoder()
        self.encoder_others = ce.OrdinalEncoder()

    def fit(self) -> None:
        self.encoder_branch.fit(self.df_train['branch'], self.df_train['price'])
        self.encoder_class.fit(self.df_train['_class'], self.df_train['price'])
        self.encoder_others.fit(self.df_train[category_other])

    def transform(self) -> None:
        self.df_train['branch'] = self.encoder_branch.transform(self.df_train['branch'])
        self.df_train['_class'] = self.encoder_class.transform(self.df_train['_class'])
        self.df_train[category_other] = self.encoder_others.transform(self.df_train[category_other])

        self.df_test['branch'] = self.encoder_branch.transform(self.df_test['branch'])
        self.df_test['_class'] = self.encoder_class.transform(self.df_test['_class'])
        self.df_test[category_other] = self.encoder_others.transform(self.df_test[category_other])

        self.df_val['branch'] = self.encoder_branch.transform(self.df_val['branch'])
        self.df_val['_class'] = self.encoder_class.transform(self.df_val['_class'])
        self.df_val[category_other] = self.encoder_others.transform(self.df_val[category_other])

    def save(self) -> None:
        save_pkl(self.encoder_branch, 'branch-func.pkl')
        save_pkl(self.encoder_class, 'class-func.pkl')
        save_pkl(self.encoder_others, 'other-func.pkl')


def preparation_data(project):
    # Load data
    run = wandb.init(project=project, job_type="data-preparation")
    artifact = run.use_artifact('train-data:latest')
    artifact_data = artifact.get("train-data")
    df_train = pd.DataFrame(columns=artifact_data.columns, data=artifact_data.data)

    artifact = run.use_artifact('val-data:latest')
    artifact_data = artifact.get("val-data")
    df_val = pd.DataFrame(columns=artifact_data.columns, data=artifact_data.data)

    artifact = run.use_artifact('test-data:latest')
    artifact_data = artifact.get("test-data")
    df_test = pd.DataFrame(columns=artifact_data.columns, data=artifact_data.data)

    # Process missing data
    mode = df_train.driver.mode()[0]
    df_train['driver'].fillna(value=mode, inplace=True)
    df_val['driver'].fillna(value=mode, inplace=True)
    df_test['driver'].fillna(value=mode, inplace=True)

    # Filter outline
    df_train = filter_outline_target(df_train)
    df_test = filter_outline_target(df_test)
    df_val = filter_outline_target(df_val)

    df_train = filter_category_feature(filter_numeric_feature(df_train))
    df_test = filter_category_feature(filter_numeric_feature(df_test))
    df_val = filter_category_feature(filter_numeric_feature(df_val))

    # Transform data
    transform = Transform(df_train, df_test, df_val)
    transform.fit()
    transform.transform()
    transform.save()

    # log transform func
    artifact = wandb.Artifact('branch-func', type='Transform')
    artifact.add_file('branch-func.pkl')
    run.log_artifact(artifact)

    artifact = wandb.Artifact('class-func', type='Transform')
    artifact.add_file('class-func.pkl')
    run.log_artifact(artifact)

    artifact = wandb.Artifact('other-func', type='Transform')
    artifact.add_file('other-func.pkl')
    run.log_artifact(artifact)

    transformed_train_df = transform.df_train[FEATURES]
    transformed_val_df = transform.df_val[FEATURES]
    transformed_test_df = transform.df_test[FEATURES]

    dataset_artifact = wandb.Artifact('transformed-train-data', type='dataset')
    dataset_table = wandb.Table(data=transformed_train_df, columns=transformed_train_df.columns)
    dataset_artifact.add(dataset_table, 'transformed-train-data')
    run.log_artifact(dataset_artifact)

    dataset_artifact = wandb.Artifact('transformed-val-data', type='dataset')
    dataset_table = wandb.Table(data=transformed_val_df, columns=transformed_val_df.columns)
    dataset_artifact.add(dataset_table, 'transformed-val-data')
    run.log_artifact(dataset_artifact)

    dataset_artifact = wandb.Artifact('transformed-test-data', type='dataset')
    dataset_table = wandb.Table(data=transformed_test_df, columns=transformed_test_df.columns)
    dataset_artifact.add(dataset_table, 'transformed-test-data')
    run.log_artifact(dataset_artifact)

    wandb.finish()