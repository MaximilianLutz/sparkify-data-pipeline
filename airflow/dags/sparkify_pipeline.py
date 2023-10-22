from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from operators.stage_redshift import StageToRedshiftOperator
from operators.load_fact import LoadFactOperator
from operators.load_dimension import LoadDimensionOperator
from operators.data_quality import DataQualityOperator
from helpers.sql_queries import SqlQueries
from airflow.models import Variable



default_args = {
    'owner': 'udacity',
    'start_date': datetime(2023, 10, 21),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
    'catchup': False,
    'email_on_retry': False
}

dag = DAG(
    'udacity_pipeline_project_mpl',
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='@hourly' 
)

start_operator = DummyOperator(task_id='Begin_execution', dag=dag)

create_tables_task = PostgresOperator(
    task_id='Create_tables',
    dag=dag,
    postgres_conn_id='redshift',
    sql=[
        SqlQueries.staging_events_table_create,
        SqlQueries.staging_songs_table_create,
        SqlQueries.songplay_table_create,
        SqlQueries.user_table_create,
        SqlQueries.song_table_create,
        SqlQueries.artist_table_create,
        SqlQueries.time_table_create
    ]
)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    table='staging_events',
    s3_bucket='udacity-dend',
    s3_key='event_data/',
    json_path='auto'
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    table='staging_songs',
    s3_bucket='udacity-dend',
    s3_key='A/A/A/',          # {{ execution_date.strftime("%Y-%m-%d") }}',  @templated time 
    json_path='auto'
)


load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='users',
    select_sql=SqlQueries.user_table_insert,
    append_mode=False
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='songplays',
    sql=SqlQueries.songplay_table_insert
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='songs',
    select_sql=SqlQueries.song_table_insert,
    append_mode=False
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='artists',
    select_sql=SqlQueries.artist_table_insert,
    append_mode=False
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='time',
    select_sql=SqlQueries.time_table_insert,
    append_mode=False
)


run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dq_checks=[
        {'check_sql': "SELECT COUNT(*) FROM users WHERE user_id is null", 'expected_result': 0},
        {'check_sql': "SELECT COUNT(*) FROM songs WHERE  song_id is null", 'expected_result': 0},
        {'check_sql': "SELECT COUNT(*) FROM artists WHERE  artist_id is null", 'expected_result': 0},
        {'check_sql': "SELECT COUNT(*) FROM songplays WHERE  songplay_id is null", 'expected_result': 0}],
    dag=dag
)

start_operator >> create_tables_task

create_tables_task >> stage_events_to_redshift
create_tables_task >> stage_songs_to_redshift

stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table

load_songplays_table >> load_user_dimension_table
load_songplays_table >> load_song_dimension_table
load_songplays_table >> load_artist_dimension_table
load_songplays_table >> load_time_dimension_table

[load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table, load_time_dimension_table] >> run_quality_checks   