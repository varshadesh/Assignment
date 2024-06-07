These instructions will help you set up and run the project on your local machine for development and testing purposes.

* Prerequisites
    Ensure you have the following installed on your machine:

    Python 3.x
    pip (Python package installer)
    PostgreSQL
    virtualenv (optional but recommended)

# Installation
1. Clone the Repository
    git clone <repository-url>
    cd <repository-directory>

2. Set Up Virtual Environment
  It is recommended to use a virtual environment to manage dependencies.

3. Set Up Virtual Environment
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

4. Install Dependencies
    pip install -r requirements.txt

5. Setting Up the Database
  1. Configure PostgreSQL
     Ensure PostgreSQL is installed and running.
     Create a new PostgreSQL database and user.
  2. Update Database Configuration
     Update the DATABASES setting in your Django settings.py file to match your PostgreSQL configuration.

      Example:


      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.postgresql',
              'NAME': 'your_db_name',
              'USER': 'your_db_user',
              'PASSWORD': 'your_db_password',
              'HOST': 'localhost',
              'PORT': '5432',
          }
      }
6.  Apply Migrations
    Run the following commands to apply the database migrations and set up your database schema:

    python manage.py makemigrations
    python manage.py migrate




8. Running the Project
    Start the development server with the following command:


    python manage.py runserver
    The server will start running at http://127.0.0.1:8000/.


