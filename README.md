# Udacity Project 5:Songify Pipeline 

## Introduction
Sparkify, a music streaming company, aims to enhance automation and monitoring of their data warehouse ETL pipelines. They've chosen Apache Airflow to create dynamic, reusable pipelines with effective monitoring and the ability for easy backfills. The source data in S3 is processed in their Amazon Redshift data warehouse, comprising JSON logs of user activity and song metadata.

This projects is designed to get familiar using airflow to orchestrate different tasks within a data pipeline for a fictional streaming service called songify. The used tools are: 
- Airflow 
- Redshift
- S3 

## Steps 


###  1 General

#### Lets go through the basic functionality of the DAG: 

1. The DAG is defined in  *sparkify_pipeline.py*. 
2. Define the default arguments for your DAG using the default args dic- tionary. For the present case this looks like this: 

```
        default_args = {
            'owner': 'udacity',
            'start_date': datetime(2023, 10, 21),
            'depends_on_past': False,
            'retries': 3,
            'retry_delay': timedelta(minutes=1),
            'catchup': False,
            'email_on_retry': False
        }
```

3. We create a new instance of the DAG class, passing the dag id, default args, and schedule interval parameters:
```
dag = DAG(
    'udacity_pipeline_project_mpl',
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='@hourly' 
) 
```

4. Define the start and end operators of your DAG:
   
```
start\_operator = DummyOperator(task\_id=’start\_execution’, dag=dag)
end\_operator = DummyOperator(task\_id=’end\_execution’, dag=dag)
```
   
5. Dont forget to set dependencies after your tasks have been written! 

### Staging the data
#### How to stage the data from S3 to Redshift:
1. Define a new operator for staging the data from S3 to Redshift. You can use the StageToRedshiftOperator provided by Udacity or create your own custom operator. Make sure the operator uses the params to generate the copy statement dynamically.
2. Add the staging operator to your DAG, specifying the task id, redshift_conn_id, aws_credentials_id, table, s3 bucket, s3_key, and other necessary parameters.
3. Set the dependencies between the staging operator and the start and end operators.

### Loading dimensions and facts
#### In this section, we’ll focus on loading dimensions and facts into Redshift.
1. Define separate operators for loading dimensions and facts. You can use the LoadDimensionOperator and LoadFactOperator provided by Udacity or create your own custom operators. Make sure the operators use the params to generate the SQL statements dynamically.
2. Add the dimension and fact operators to your DAG, specifying the task id, redshift conn id, table, sql query, and other necessary parameters.
Set the dependencies between the dimension and fact operators and the staging operator.


Database Structure: 
<img src= songify.png></img>

### Data Quality Checks
#### In this section, we’ll focus on performing data quality checks on the loaded data.
1. Define an operator for data quality checks. You can use the DataQualityOperator provided by Udacity or create your own custom operator. Make sure the operator uses the params to get the tests and results dynamically.
2. Add the data quality operator to your DAG, specifying the task id, redshift conn id, tests, and other necessary parameters.
Set the dependencies between the data quality operator and the dimension and fact operators.


### Testing and Running the DAG
1. Before running the DAG, make sure you have set up Airflow correctly and have the necessary connections and variables configured.
2. Start the Airflow scheduler and webserver.
3. Access the Airflow UI and verify that your DAG is visible without any issues.
