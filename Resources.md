Step 1: Install Apache Airflow
You can install Apache Airflow using pip. It’s recommended to install Airflow in a virtual environment.

pip install apache-airflow


Step 2: Configure Apache Airflow
After installing, you need to initialize the Airflow database and create the necessary folders.

# Initialize the database
airflow db init

# Create the necessary folders
mkdir -p ~/airflow/dags ~/airflow/logs ~/airflow/plugins
