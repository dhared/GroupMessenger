# Messenger
A simple app that provides apis for group chat.

## Installation
This app is built on top of `python3.10`. You can install this python from any package manager depending on your os.

After installation of python. Run following commands:

```bash
# Clone this repo
git clone <project_repo>

# Change directory to the project root 
cd messenger

# Install dependency modules
pip install -r requirements.txt
```

## Admin User
To interact with the app you will need an admin user. Run below command to create one:
```bash
python manage.py createsuperuser
```
This will ask you few details of admin user, fill this up and your user will get created.

## Run Server
```bash
python manage.py runserver
```
This will start development server on your machine at port 8000. 
visit admin panel at http://localhost:8000/admin

## API Documentation
You can install postman from [here](https://www.postman.com/downloads/). Open postman and import the collection file
with name *postman_collection.json* from the repo.