# Newsletter App

The Newsletter App is a web application that displays newsletters from various companies. It serves as a valuable resource for research, whether you are writing your own newsletter or looking for discounts and promotions from different businesses. The app is built using Python, Streamlit, and SQLite.

## Setup

To get started with the Newsletter App, follow these steps:

1. Clone the repository to your local machine:
```bash
git clone <repository-url>
cd newsletter-app
```

2. Create a file called `credentials.env` in the root folder and add the following content, replacing "XXX" with your actual email server, username, and password:
```bash
EMAIL_SERVER = "XXX"
EMAIL_USER = "XXX"
EMAIL_PASSWORD = "XXX"
```
This step is necessary to set up the email functionality for the app. Information about the IMAP email server can be found [here](https://www.systoolsgroup.com/imap/).

## Installation and Setup

To run the Newsletter App, you need to ensure you have [Poetry](https://python-poetry.org/) installed. Poetry is a dependency management and packaging tool for Python. If you haven't installed it yet, follow the instructions on their website for your specific operating system.

After installing Poetry, navigate to the root folder of the project and run the following command to set up the virtual environment and install the required dependencies:

```
poetry install
```

Once the dependencies are installed, you can activate the virtual environment by running:

```
poetry shell
```
## Initialize the Database

To get the Newsletter App up and running with the latest company information and email data, follow these steps:

### 1. Companies CSV File

The `companies.csv` file contains information about various companies. Before initializing the database, ensure that this CSV file is updated with the latest company information. You can modify the existing entries or add new ones as needed.

### 2. Adding Companies to the Database

To add the companies from the `companies.csv` file to the SQLite database, run the following command in the venv:
```
python3 add_company.py
```

### 3. Importing Emails Daily

To keep the app up to date with the latest emails, you can set up a scheduled task using a Lambda function (if deploying on a cloud platform) or a cron job (if deploying on a server). The `read_mail.py` script will be executed every day to import emails from the previous day. Here's an example of a cron job:
```
0 6 * * * cd location/of/newsletter_app/ && poetry run python3 read_mail.py
```
n the above cron job, the script `read_mail.py` is set to run every day at 6:00 AM. Make sure to replace `location/of/newsletter_app/` with the actual path to the root folder of your Newsletter App project.

### 4. Site Ready to Display Companies and Emails

Once the `add_company.py` script is executed to populate the database with company information and the `read_mail.py` script is set up to import emails daily, your site should be ready to display companies and their corresponding emails.
## Running the App

With the virtual environment activated, you can now start the Newsletter App using the following command:

```
streamlit run app.py
```

This will launch the app, and you can access it through your web browser at `http://localhost:8501`.

## Live Example

Check out the live example of the Newsletter App [here](http://13.53.108.5:8501/).

Please note that this link might not be active indefinitely, as it is a live instance and could be taken down at any time.

## Contact

If you have any questions or need further assistance, please don't hesitate to contact me at [nicolas.neudeck@outlook.de](mailto:nicolas.neudeck@outlook.de) or on [LinkedIn](https://www.linkedin.com/in/nicolasneudeck/).

Happy exploring and enjoy using the Newsletter App!