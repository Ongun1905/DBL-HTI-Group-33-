<div align="center">
  <h1>DBL HTI + WEBTECH - Group 33</h1>
  <i>Interactive visualisation of a dynamic network</i>
</div>
<br>
<br>

# Project website: https://dblgroup33.herokuapp.com/ 
Warning: we are using heroku free plan so users might have to wait a few seconds to wake up the app. 


# Usage to run website locally 
To run the web app locally, there are a few steps that need to be followed. Using a Python virtual environment is recommended<sup>1</sup> but not required. If you don't want to use a virtual environment, skip the "(Optional) Python virtual environment setup" step.

## Installation
### <a name="python-venv-setup"></a> (Optional) Python virtual environment setup
Install the `virtualenv` package and create a virtual environment. Both are explained in [this guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for Windows, macOS and Linux. Make sure to activate the virtual environment before continuing to the next steps!

For more information about virtual environments in Python, you can read the [documentation](https://docs.python.org/3/tutorial/venv.html).

### Installing the required packages
1. Open up a console and navigate to the root of this repository
2. Install the required packages for the web app using `pip install -r requirements.txt`

## Starting the web app on a local server
1. Open up a console and navigate to the root of this repository
2. Enter `python DBL_Project/dbl/manage.py runserver`

After a few seconds, the console log should look similar to this:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 20, 2021 - 14:41:07
Django version 3.2, using settings 'dbl.settings'
Starting ASGI/Channels version 3.0.3 development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Follow the link in the console output (http://127.0.0.1:8000/) to view the web app in action!

# Feature explanation
This tool is a web-based network visualization application. It contains 2 visualizations: A node-link diagram and an adjacency matrix. The beginnings of a data upload tool can be seen on the frontpage, but the source code still uses a static file in the source directory.


<hr>
1. Using a virtual environment is recommended since this web app uses specific versions of certain packages. Using a virtual environment isolates Python files on a per-project basis, which ensures that no package version conflicts can occur.
