# Newsletter App

The Newsletter App is a web application that displays newsletters from various companies. It serves as a valuable resource for research, whether you are writing your own newsletter or looking for discounts and promotions from different businesses. The app is built using Python, Streamlit, and MongoDB.

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

## Running the App

With the virtual environment activated, you can now start the Newsletter App using the following command:

```
streamlit run app.py
```

This will launch the app, and you can access it through your web browser at `http://localhost:8501`.

## Live Example

Check out the live example of the Newsletter App [here](http://www.example-newsletter-app.com).

Please note that this link might not be active indefinitely, as it is a live instance and could be taken down at any time.

& Contact

If you have any questions or need further assistance, please don't hesitate to contact us at [nicolas.neudeck@outlook.de](mailto:nicolas.neudeck@outlook.de).

Happy exploring and enjoy using the Newsletter App!