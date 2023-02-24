import os
import wandb
import pandas as pd

import pkg_resources
import importlib

import tensorflow_data_validation as tfdv
from sklearn.model_selection import train_test_split
from tensorflow_data_validation.utils.display_util import get_statistics_html

import warnings
warnings.filterwarnings("ignore")
importlib.reload(pkg_resources)

_CLASS = ['Ranger', 'Morning', 'Vios', 'Innova', 'Camry', 'C class', 'i10', 'Fortuner', 'SantaFe', 'E class', '3', 'GLC', 'Everest', 'Accent', 'CX5', 'Corolla altis', 'CRV', 'Lux A 2.0', 'S class', 'Cerato', 'Spark', 'RX', 'Tucson', 'City', 'Civic', 'Fadil', 'Xpander', 'Elantra', 'Lux SA 2.0', 'Corolla Cross', 'Yaris', 'Lacetti', 'Cruze', 'Transit', '6', 'Explorer', 'EcoSport', 'Prado', 'K3', 'Triton', 'Sorento', '5 Series', 'Range Rover', 'Outlander', 'Land Cruiser', 'BT50', 'Seltos', 'LX', '-', '3 Series', '2', 'Matiz', 'Focus', 'Attrage', 'Cayenne', 'Jolie', 'Captiva', 'Getz', 'ZS', 'Carens', 'Navara', 'Creta', 'Soluto', 'Escape', 'Hilux', 'Forte', 'XL7', 'Veloz', 'ES', 'Carnival', 'Khác', 'Rio', 'CX8', 'Zace', 'Pajero Sport', 'Swift', 'Wigo', 'Kona', '7 Series', 'Gentra', 'Rondo', 'Range Rover Evoque', 'Super Carry Truck', 'Macan', 'Panamera', 'Fiesta', 'GX', 'Dmax', '3008', 'Frontier', 'Carry', 'Porter', 'Aveo', 'Avanza', 'Accord', 'Almera', 'Sonet', 'Tiguan', 'X5', 'Hiace', 'G class', 'Avante', 'Raize', 'Super Carry Van', 'Colorado', 'Cooper', 'GLS', 'Ertiga', 'Laser', 'Sienna', 'Brio', 'Rush', 'HS', 'VF e34', 'Corolla', 'Mondeo', 'XC90', 'Q7', '5', 'NX', 'Grandis', 'Sedona', 'QKR', 'Maybach', 'cx3', 'Forester', 'Pajero', 'X6', 'LS', 'i20', 'Sunny', 'XC60', 'Optima', '5008', 'Nubira', 'K3000S', 'Towner', 'MU-X', 'County', 'GLE Class', 'GLB', '323', 'Lanos', 'GL', 'X trail', 'Orlando', 'Wrangler', 'Mighty', 'V class', 'X1', 'Polo', 'Grand Starex', 'Range Rover Sport', 'HD', 'CLA class', 'Q5', 'HRV', 'Venza', 'CX 30', 'Spectra', 'Vivant', '2008', 'Sonata', 'Teana', 'A4', '626', 'A6', 'X4', 'K5', 'Sprinter', 'Ciaz', 'VF9', 'Jazz', 'Flying Spur', 'X7', 'GLK Class', 'Hi lander', 'i30', 'Pride', 'X3', 'VF8', 'Z4', 'GLA class', 'F150', 'RAV4', 'Zinger', 'Levante', 'Phantom', 'XC40', 'Vitara', 'Teramont', 'K2700', 'Ghost', 'Magnus', 'Starex', 'MDX', '4 Series', 'Citivan', '718', 'Alphard', 'Verna', 'Lancer', 'IS', 'Mulsanne', 'Cressida', 'Passat', 'Mirage', 'Siena', 'A8', 'Grand livina', 'Ollin', 'Celerio', 'Tourneo', 'Picanto', 'Forland', 'Musso', 'Sportage', 'Libero', 'A class', 'Solati', 'Terra', 'APV', 'Range Rover Velar', 'Crown', 'Corona', 'Discovery Sport', 'Ghibli', 'DB1021', 'DB X30', '911', 'Highlander', 'Outback', 'President', 'Genesis', 'Bentayga', 'Trailblazer', 'GS', 'Mustang', 'S90', 'Defender', 'Escalade', 'QX', 'Foton', 'XJ series', 'Tundra', 'Bongo', 'NQR', 'A5', 'NPR', 'Veloster', 'Quattroporte', 'One', 'Cullinan', 'Trooper', 'Terios', 'Juke', 'Q3', 'Universe', 'MB', 'Traveller']
_BRANCH = ['Toyota', 'Hyundai', 'Kia', 'Ford', 'Mercedes Benz', 'Mazda', 'Honda', 'Mitsubishi', 'VinFast', 'Chevrolet', 'Lexus', 'BMW', 'Daewoo', 'Suzuki', 'Nissan', 'Porsche', 'LandRover', 'Isuzu', 'MG', 'Audi', 'Peugeot', 'Volkswagen', 'Hãng khác', 'Volvo', 'Thaco', 'Mini', 'Subaru', 'Bentley', 'Rolls Royce', 'Maserati', 'Jeep', 'Ssangyong', 'Daihatsu', 'Dongben', 'Fiat', 'Jaguar', 'Acura', 'Infiniti', 'Vinaxuki', 'Cadillac', 'Lincoln', 'Chrysler', 'Baic', 'Renault', 'JRD', 'Lamborghini', 'Chery', 'Luxgen', 'SYM', 'RAM']


def infer_schema(project: str, artifact_name='raw-dataset:latest', filename='raw-dataset', is_running=True, run=None):
    # Initialize a new W&B run to track this job
    if not is_running:
        run = wandb.init(project=project, job_type="infer-schema")

    # Create a sample dataset to log as an artifact
    artifact = run.use_artifact(artifact_name)
    artifact_data = artifact.get(filename)
    df = pd.DataFrame(columns=artifact_data.columns, data=artifact_data.data)

    df.drop(['_id', '_url', 'datetime'], axis=1, inplace=True)
    df = df.loc[df['color_exterior'] != '-']
    df = df.loc[df['color_furniture'] != '-']
    df['branch'] = df.branch.apply(lambda x: x if x in _BRANCH else 'other')
    df['_class'] = df._class.apply(lambda x: x if x in _CLASS else 'other')
    

    train_df, test_df = train_test_split(df, train_size=0.9, shuffle=True, random_state=43, stratify=df['branch'])
    train_stats = tfdv.generate_statistics_from_dataframe(dataframe=train_df)
    schema = tfdv.infer_schema(statistics=train_stats)
    schema_df_result = tfdv.utils.display_util.get_schema_dataframe(schema=schema)

    # log schema
    artifact = wandb.Artifact('categorical-schema', type='Schema')
    categorical_schema = schema_df_result[1].reset_index()
    schema_table = wandb.Table(data=categorical_schema, columns=categorical_schema.columns)
    artifact.add(schema_table, 'categorical-schema-table')
    run.log_artifact(artifact)

    artifact = wandb.Artifact('data-schema', type='Schema')
    data_schema = schema_df_result[0].reset_index()
    schema_table = wandb.Table(data=data_schema, columns=data_schema.columns)
    artifact.add(schema_table, 'data-schema-table')
    run.log_artifact(artifact)

    tfdv.write_schema_text(schema=schema, output_path='schema.txt')
    artifact = wandb.Artifact('text-schema', type='Schema')
    artifact.add_file('schema.txt')
    run.log_artifact(artifact)

    if not is_running:
        wandb.finish()
    else:
        return schema


def get_schema(project, artifact_name='text-schema:latest', is_running=True, run=None):
    if not is_running:
        run = wandb.init(project=project, job_type="download-schema")
    schema = None

    try:
        artifact = run.use_artifact(artifact_name)
        artifact_dir = artifact.download()
        schema = tfdv.load_schema_text(os.path.join(artifact_dir, 'schema.txt'))
        if not is_running:
            wandb.finish()
    except:
        if not is_running:
            wandb.finish(exit_code=1)
        pass

    return schema


def validate_data(project):
    run = wandb.init(project=project, job_type="data-validation")
    # Pull down that dataset you logged in the last run
    artifact = run.use_artifact('raw-dataset:latest')
    artifact_data = artifact.get("raw-dataset")
    df = pd.DataFrame(columns=artifact_data.columns, data=artifact_data.data)

    # remove unexpected values
    df.drop(['_id', '_url', 'datetime'], axis=1, inplace=True)
    df = df.loc[df['color_exterior'] != '-']
    df = df.loc[df['color_furniture'] != '-']
    df['branch'] = df.branch.apply(lambda x: x if x in _BRANCH else 'other')
    df['_class'] = df._class.apply(lambda x: x if x in _CLASS else 'other')

    # split data
    train_df, test_df = train_test_split(df, train_size=0.9, shuffle=True, random_state=43, stratify=df['branch'])
    train_df, val_df = train_test_split(train_df, train_size=0.85, shuffle=True, random_state=43,
                                        stratify=train_df['branch'])

    # log train, val, test data
    dataset_artifact = wandb.Artifact('train-data', type='dataset')
    dataset_table = wandb.Table(data=train_df, columns=train_df.columns)
    dataset_artifact.add(dataset_table, 'train-data')
    run.log_artifact(dataset_artifact)

    dataset_artifact = wandb.Artifact('val-data', type='dataset')
    dataset_table = wandb.Table(data=val_df, columns=val_df.columns)
    dataset_artifact.add(dataset_table, 'val-data')
    run.log_artifact(dataset_artifact)

    dataset_artifact = wandb.Artifact('test-data', type='dataset')
    dataset_table = wandb.Table(data=val_df, columns=val_df.columns)
    dataset_artifact.add(dataset_table, 'test-data')
    run.log_artifact(dataset_artifact)

    schema = get_schema(run=run, project=project, is_running=True)
    if schema is None:
        schema = infer_schema(
            run=run,
            project=project,
            artifact_name='raw-dataset:latest',
            filename='raw-dataset',
            is_running=True
        )

    # generate statistics
    train_stats = tfdv.generate_statistics_from_dataframe(dataframe=train_df)
    eva_stats = tfdv.generate_statistics_from_dataframe(dataframe=val_df)
    serving_stats = tfdv.generate_statistics_from_dataframe(dataframe=test_df)

    # log statistics
    file = get_statistics_html(lhs_statistics=eva_stats,
                               rhs_statistics=train_stats,
                               lhs_name='VAL_DATASET',
                               rhs_name='TRAIN_DATASET')
    artifact = wandb.Artifact('statistic', type='Statistic')
    html = wandb.Html(data=file)
    artifact.add(html, 'Statistic')
    run.log_artifact(artifact)

    # detect anomalies
    val_anomalies = tfdv.validate_statistics(
        statistics=eva_stats,
        schema=schema
    )
    val_anomalies = tfdv.utils.display_util.get_anomalies_dataframe(val_anomalies).reset_index()

    serving_anomalies = tfdv.validate_statistics(serving_stats, schema)
    serving_anomalies = tfdv.utils.display_util.get_anomalies_dataframe(serving_anomalies).reset_index()

    # log anomalies
    anomalies_table = wandb.Table(data=val_anomalies, columns=val_anomalies.columns)
    run.log({"Val anomalies": anomalies_table})

    anomalies_table = wandb.Table(data=serving_anomalies, columns=serving_anomalies.columns)
    run.log({"Serving anomalies": anomalies_table})

    wandb.finish()