--To Run the application:

--create a virtual environment inside the project folder

python -m venv env

--activate that virtual environment

env\Scripts\activate

--install the dependencies inside the activated virtual environment

pip install -r requirements.txt

--run the application:

python app.py -- for flask app
python manage.py -- for django project 

--On first run, an admin user will automatically be created:
- Username: anu
- Password: 123

-- now the project will open and it shows homepage, reviews, courses, chat bot 
-- it also has the functionality to reset the password in your django project 


--  created api for reviews and courses 

--To test the following endpoints use the Postman software or any HTTP client tool

for reviews--> api/reviews
for courses--> api/courses





