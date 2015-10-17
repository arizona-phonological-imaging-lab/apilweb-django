# apil-web

#####

# How to run the app

## Accessing the test database

To interact with the test database, you will need the [Git Large File Storage extensions](https://git-lfs.github.com/).  This is the recommended way to handle large files (or files that could eventually become quite large).

For OSX users, the extension can be installed via `homebrew`:  

`brew install git-lfs`

## Install `virtualenv` for python 3.x

On OSX, install `python3` via homebrew:  

`brew install python3`  

Install virtualenv with `pip`:  

`pip install virtualenv`  

## Create a virtual environment

From the project directory, enter the following command:

`virtualenv -p python3 venv`  

## Activate the virtual environment
### 1) Activating the python virtual environment  

From the project directory, `source venv/bin/activate`

### 2) Installing the project dependencies

After activating the vm, make sure you have all of the necessary dependencies installed.  Simply type:  
`pip install -r requirements.txt`  

### 3) Run the web app locally

  1. From the project directory, type:  
`python manage.py runserver`  
  2. In your browser, navigate to `http://localhost:8000`

### 4) Creating an admin user

Use the following command to create a new admin user:  

`python manage.py createsuperuser`  

### 4) Adding dependencies

Install a new package:  

`pip install <some package name here>`

Update `requirements.txt`:  
`pip freeze > requirements.txt`

Be careful not to add unnecessary dependencies to `requirements.txt`
## Exiting the virtual environment

`deactivate`

# Active apps
This section describes our current working apps.  

### `UATracker`

You may view a sample of database entries at this url:  

http://localhost:8000/uat/1/

# Developing new apps

Please develop your app on a branch:

If you were making an app called `analysis`, branch off of master in the following way:

`git checkout master`
`git checkout -b analysis`

Make your app and test it.  

`python mange.py startapp analysis`  

When you're ready, merge it into master:

`git checkout master`

Remember to `pull`!

`git pull`

Now merge:

`git merge analysis`

If the merge is successful (or you've resolved any conflicts), go ahead and `push`:

`git push`

...and update the `README`!
