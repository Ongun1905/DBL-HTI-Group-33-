<div align="center">
  <h1>DBL HTI + WEBTECH - Group 33</h1>
  <i>Interactive visualisation of a dynamic network</i>
</div>
<br>
<br>

# Usage
In order to run the webapp, there's a few steps that need to be followed. Using a Python virtual environment is recommended<sup>1</sup> but not required.

## Installation
### <a name="python-venv-setup"></a> Python virtual environment setup
1. Open up a console and navigate to the root of this repository
2. Create a new virtual environment by entering `python -m venv venv`. This will create a virtual environment with the name "venv" in the repository root.
3. Start the virtual environment by entering `venv\Scripts\activate.bat`

For more information about virtual environments in Python, you can read the [documentation](https://docs.python.org/3/tutorial/venv.html).

### Installing the required packages
1. Open up a console and navigate to the root of this repository
2. Install the required packages for the webapp using `pip install -r requirements.txt`

## Starting the webapp
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

Follow the link in the log (http://127.0.0.1:8000/) to view the webapp in action!
<hr>
1. Using a virtual environment is recommended since this webapp uses specific versions of certain packages. Using a virtual environment isolates Python files on a per-project basis, which ensures that no package version conflicts can occur.