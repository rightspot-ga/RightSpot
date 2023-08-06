# RightSpot

## Description
This was the third project completed as part of the General Assembly SEI Bootcamp. The goal of the project was to create a web app with full CRUD (create, read, update, delete) functionality. Django was to be used for the server, with a PostgreSQL database. Drawing inspiration from the  issues some of my friends faced when opening a cafe, I wanted to create a user-friendly app that could assist entrepreneurs with selecting a location for their business by providing useful statistical data compiled from multiple sources, all in one place.

## Deployment link
The project is hosted [here](https://rightspot.fly.dev/).

## Project Setup Instructions
1. Clone the project repository:
```bash
git clone https://github.com/andy-ag/RightSpot.git
```

2. Navigate to the root directory of the project:
```bash
cd RightSpot
```

3. Create a virtual environment for the project:
```bash
python -m venv env
```

4. Activate the virtual environment:

On Linux/Mac:
```bash
source env/bin/activate
```
On Windows:
```bash
env\Scripts\activate
```

5. Install the required dependencies:
```bash
pip install -r requirements.txt
```

6. Set up environment variables:
Create a .env file in the RightSpot app directory of the project and add the required environment variables.

The variables are listed in the prerequisites, or you can copy the .env copy file and modify it with your values.

7. Run the database migrations:
```bash
python manage.py migrate
```

8. Create a superuser account:
```bash
python manage.py createsuperuser
```

Follow the prompts to enter your username, email, and password.

9. Start the development server:
```bash
python manage.py runserver
```

10. View the website:

Open your web browser and navigate to http://localhost:8000/ to view the website.



