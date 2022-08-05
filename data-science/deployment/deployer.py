
import os
import joblib
import shutil
import tarfile
import numpy as np
from sklearn.base import BaseEstimator
from sagemaker.sklearn import SKLearnModel
from metaflow import S3
from dotenv import load_dotenv
load_dotenv('my.env')

def to_sagemaker(
    model:BaseEstimator = None,
    sagemaker_model_name:str = "model",
    model_save_name:str = "model", 
    endpoint_name:str = "sklearn endpoint", 
    instance_type:str = "ml.c5.2xlarge", 
    entry_point:str = "sagemaker_entry_point.py",
    sklearn_version:str = "1.0-1",
    role:str = os.getenv('ROLE'), 
    code_location:str = os.getenv('CODE_LOCATION'),
    run = None,
):

    # save model to local folder
    # this should match what is in sagemaker_entry_point
    model_save_name = "model"
    os.makedirs(model_save_name, exist_ok=True)
    out_path = "{}/{}.joblib".format(model_save_name, model_save_name)
    joblib.dump(model, out_path)
    
    # save model as tar.gz
    local_tar_name = "{}.tar.gz".format(model_save_name)
    with tarfile.open(local_tar_name, 
                      mode="w:gz") as _tar:
        _tar.add(model_save_name, recursive=True)

    # save model onto S3
    with S3(run=run) as s3:
        with open(local_tar_name, "rb") as in_file:
            data = in_file.read()
            model_s3_path = s3.put(local_tar_name, data)

    # remove local model folder and tar
    shutil.rmtree(model_save_name)
    os.remove(local_tar_name)
    
    print("Creating and deploying Sagemaker model...")
    sklearn_model = SKLearnModel(
        name=sagemaker_model_name,
        model_data=model_s3_path, 
        role=role,
        entry_point=entry_point,
        framework_version=sklearn_version,
        code_location=code_location
    )
    
    predictor = sklearn_model.deploy(
        instance_type=instance_type,
        initial_instance_count=1,
        endpoint_name=endpoint_name
    )
    
    return model_s3_path
