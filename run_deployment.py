from typing import cast
from pipelines.deployment_pipeline import deployment_pipeline, inference_pipeline
from zenml.integrations.mlflow.mlflow_utils import get_tracking_uri
from zenml.integrations.mlflow.model_deployers.mlflow_model_deployer import(
    MLFlowModelDeployer, mlflow_model_deployer_component
)
from pipelines.deployment_pipeline import continuous_deployment_pipeline
from zenml.integrations.mlflow.services import MLFlowDeploymentService
import click

DEPLOY = "deploy"
PREDICT = "predict"
DEPLOY_AND_PREDICT = "deploy_and_predict"

@click.command()
@click.option(
    "--config",
    "-c",
    type = click.Choice([DEPLOY, PREDICT, DEPLOY_AND_PREDICT]),
    default = DEPLOY_AND_PREDICT,
    help = "Optionally you can choose to run deployment or prediction seperately"
)
@click.option(
    "--min-accuracy",
    default = 0.92,
    help = "Minimum acc required to deploy the model",
)

def run_deployment(config : str, min_accuracy: float):
    deployer = MLFlowModelDeployer.get_active_model_deployer()
    deploy = config == DEPLOY or config == DEPLOY_AND_PREDICT
    predict = config == PREDICT or config == DEPLOY_AND_PREDICT

    if deploy:
        continuous_deployment_pipeline(data_path= "Data/olist_customers_dataset.csv",
                                        min_accuracy = min_accuracy,
                                       workers = 3,
                                       timeout = 60,)
    if predict:
        inference_pipeline()

    print("You can run:\n"
          f"[italic green] mlflow ui --backend-store-uri {get_tracking_uri()}")
    

    existing_services = mlflow_model_deployer_component.find_model_server(
        pipeline_name = "continuous_deployment_pipeline",
        pipeline_step_name = "mlflow_model_deployer_step",
        model_name = "model"
    )
    if existing_services:
        service = cast(MLFlowDeploymentService, existing_services[0])
        if service.is_running:
            print(f"The MLFlow prediction server is running locally as a daemon"
                  f"process service and accepts inference requests at:\n"
                  f"     {service.prediction_url}\n"
                  f"To stop the service, run"
                  f"[italic green]`zenml model-deployer models delete"
                  f"{str(service.uuid)}`[/italic green].")
        elif service.is_failed:
            print(
                f"The MLFlow prediction server is in a failed state:\n"
                f"Last state: '{service.status.state.value}'\n"
                f"Last error: '{service.satus.last_error}'"
            )
    else:
        print(
            "No Server running"
        )

run_deployment()