# GITHUB CONFIGURATIN

Configuring your user.name and user.email in Git is important for proper identification in your commits. Here's how you can do it:

Global Configuration (affects all repositories):

Open your terminal.
Run the following command, replacing "Your Name" with your actual name and "you@example.com" with your email address:
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
Repository-Specific Configuration (affects only that repository):

Navigate to your Git repository directory using the cd command.
Run the same commands as above, but without the --global flag:
git config user.name "Your Name"
git config user.email "you@example.com"
Verifying Configuration:

You can verify your current configuration using:

git config --list
This will display all Git settings, including your user.name and user.email.

Using Environment Variables (temporary):

Alternatively, you can set environment variables for the current session:

export GIT_AUTHOR_NAME="Your Name"
export GIT_AUTHOR_EMAIL="you@example.com"
Remember:

Using the global configuration is recommended for most cases.
Make sure to use a valid email address associated with your Git hosting platform (e.g., GitHub, GitLab).


# APACHE AIRFLOW CONFIGURATION
Step 1: Install Apache Airflow
You can install Apache Airflow using pip. It’s recommended to install Airflow in a virtual environment.

pip install apache-airflow


Step 2: Configure Apache Airflow
After installing, you need to initialize the Airflow database and create the necessary folders.

# Initialize the database
airflow db init

# Create the necessary folders
mkdir -p ~/airflow/dags ~/airflow/logs ~/airflow/plugins
