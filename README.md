# booking

## About

This is an application for booking cars through a RESTful API.  


## Installation

Clone this git repo

```
$ git clone https://github.com/johanlundahl/booking
```


## Requirements

Install required python modules

```
$ pip install -r requirements.txt
```


Create a config.py file in the root to store application specific parameters required by the application
```
db_name = 'sqlalchemy.db'
db_uri = 'sqlite:///{}'.format(db_name)
```

Create the database 
```
$ python cmd.py -create
```

## Run

To run the application type

```
$ python app.py
```

The endpoints of the API are available at http://localhost:5000/api.

