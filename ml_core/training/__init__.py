import wandb
import numpy as np
import pandas as pd
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


n_estimators = [int(x) for x in np.linspace(start = 20, stop = 300, num = 10)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}


def train(project, is_test=False):
    run = wandb.init(project=project, job_type='training')

    artifact = run.use_artifact('transformed-train-data:latest')
    artifact_data = artifact.get("transformed-train-data")
    df_train = pd.DataFrame(columns=artifact_data.columns, data=artifact_data.data)

    artifact = run.use_artifact('transformed-test-data:latest')
    artifact_data = artifact.get("transformed-test-data")
    df_test = pd.DataFrame(columns=artifact_data.columns, data=artifact_data.data)

    if is_test:
        df_train = df_train.head(100)
        df_test = df_test.head(100)
    X_train = df_train.drop(['price'], axis=1)
    y_train = df_train['price']

    X_test = df_test.drop(['price'], axis=1)
    y_test = df_test['price']

    rf = RandomForestRegressor()
    # Random search of parameters, using 3 fold cross validation,
    # search across 100 different combinations, and use all available cores
    rf_random = RandomizedSearchCV(estimator=rf, param_distributions=random_grid, n_iter=20, cv=5, verbose=2,
                                   random_state=42, n_jobs=-1)

    rf_random.fit(X_train, y_train)
    best_model = rf_random.best_estimator_

    y_preds = best_model.predict(X_test)
    mae = mean_absolute_error(y_preds, y_test)
    mse = mean_squared_error(y_preds, y_test)
    r2 = r2_score(y_preds, y_test)

    wandb.sklearn.plot_feature_importances(best_model, list(df_train.columns))
    wandb.config.update(rf_random.best_params_)
    wandb.config.update({'mse-test': mse, 'mae-test': mae, 'r2-test': r2})

    # log best model
    with open('model.pkl', 'wb') as file:
        pickle.dump(best_model, file)

    artifact = wandb.Artifact('model', type='Model')
    artifact.add_file('model.pkl')
    run.log_artifact(artifact)

    wandb.finish()