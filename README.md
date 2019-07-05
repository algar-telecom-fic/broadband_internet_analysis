# broadband_internet_analysis
Application for broadband internet analysis automation


# Interface

The interface is built in [Python3.6](https://www.python.org/downloads/) using the [Flask](http://flask.pocoo.org/) microframework.
This guide will show how to setup the enviroment and run the interface. For further learning about Flask I recommend checking out this [video tutorial](https://www.youtube.com/playlist?list=PL3BqW_m3m6a05ALSBW02qDXmfDKIip2KX).

## First install virtualenv (recommend):

This step creates a virtual enviroment. This basically creates a different python installation to allow you to install the python version you need and install the packages you need in the version you need, without the risk of having conflicting versions or packages messing up your local python installation and interfering in your other projects.

### Install **pip** first
pip is the python package installer, you are going to use this to install the Flask package and many other insteresting stuff.

    sudo apt-get install python3-pip

### Then install **virtualenv** using pip3

    sudo pip3 install virtualenv 

### Now create a virtual environment 

    virtualenv venv 

>you can use any name insted of **venv**

### You can also use a Python interpreter of your choice

    virtualenv -p /usr/bin/python3.6 venv

### Create virtualenv using Python3
    
    virtualenv -p python3 myenv
    
### Active your virtual environment:    
    
    source venv/bin/activate

### To deactivate:

    deactivate

### Once the virtualenv is installed and activated, install the requirements
Inside the Interface folder in this project there is a *requirements.txt* file. This file have all the packages you must install to the run the project. You can install them all at once using pip3
    
    pip3 install -r requirements.txt


-------------------
## Run the interface

In your local enviroment you can run the app easily, just run the file *run.py*

    python3 run.py

In production enviroment, though, you're going to need something more reliable. We'are using gunicorn, install it and run with   

    python3 -m gunicorn.app.wsgiapp -w 4 -b 0.0.0.0:5000 app:app

This is going to run in the port 5000. Be aware that your firewall must have this port open for you to access this address from another machine
