# Waste Management System

## Installation

To install the project, follow these steps:

1. Make sure you have [Python](https://www.python.org/) installed on your system.
2. Clone the repository to your local machine.
3. Open a terminal and navigate to the project directory.
4. Run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```


## Getting Started

To run the project, follow these steps:

### A. Create the Database

1. Run the following commands to create the database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```


### B. Create a Superuser

1. Create a superuser account that will have administrative privileges by running the following command:
```bash
python manage.py createsuperuser
```

Follow the prompts to enter the username and password for the superuser.

### C. Run the Server

1. Start the development server by running the following command:
```bash
python manage.py runserver
```


### D. Set Up Areas

1. Access the admin panel by visiting `http://localhost:8000/admin` in your web browser.
2. Log in using the superuser credentials created earlier.
3. Create new areas that correspond to different regions or locations for waste collection.

### E. Create Collector Accounts

1. Access the registration page of the application by visiting `http://localhost:8000/register` in your web browser.
2. Create a new collector account for each area defined in the previous step.

### F. Create User Accounts

1. Access the registration page of the application by visiting `http://localhost:8000/register` in your web browser.
2. Create a new user account for each area defined in the previous step.

### G. Login

1. Access the login page of the application by visiting `http://localhost:8000/login` in your web browser.
2. Log in using the credentials of a collector or user account.

## Usage

Once logged in, users and collectors can perform various actions based on their respective roles. Users can request waste collection, view collection history, and manage their account. Collectors can view assigned collection requests, update the status of collections, and manage their account.

## Contributing

Contributions to the Waste Management System project are welcome! provided that you've been granted with access!!. If you have any ideas, suggestions, or bug reports, please open an issue on the project's GitHub repository.

## License

This project is Private licensed.

