# FLASK RESTFUL API Simple Linear Regression

Here contains code for a Restful API built using the Flask_Restful extension to Flask. This will include the following features:
- Building a simple Linear Regression model
- User authentication for certain requests
- Add or delete users
- Make predictions with the linear regression model
- Add more data to the database (and retrain if necessary)
- Reset the database with original data entries 

## Instructions

Deploy the contents of this repository to Heroku to have an API on a server. Alternatively, download this repository and use the following command on your terminal in the same directory:

```
python app.py
```

This should run the application and place the API on a local server (port = 5000 by default).

### Calling the API

This can be done using CURL commands on terminal, however, I find using [Postman](https://www.postman.com/) much easier. 

When getting predictions, use the following format for the JSON data entry.
```
{"input_data":[{"fields":["age","sex","cp","trestbps","chol",
"fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"],
"values":[[1,1,1,1,0,5,1231,1,1,1,1,1,1]]}]}
```


# API details
The following classes can be found in the resources folder:
- add_data.py : this allows you to add data to the database
- create_tables.py : this will create a database to store the training data and username & passwords if one does not exist already
- db.py : this initiates the Flask_SLQAlchemy connection
- predict.py : this will allow you to send JSON data and retrieve a prediction from the lin reg model
- security.py : this will authenticate the user to provide a JSON web token (JWT)
- train.py : this will train the model or retrain the model with new data
- user.py : this will find, get and delete users from the database

# Heroku files
The following files were written for the purpose of deploying the API on Heroku's server. 
- requirements.txt : this contains all the python libraries that need to be installed in order to run the app
- uwsgi.ini : Heroku does not provide a web server of its own. Instead, it expects the application to start its own web server on the port number given in the environment variable $PORT. Since the Flask development web server is not robust enough to use for production, I'm using [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/) here. 
- runtime.txt : this tells Heroku the version of Python you are using
- Procfile : this will give instructions to Heroku to run the app using uwsgi
