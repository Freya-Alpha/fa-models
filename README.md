# fa-models
A set of models often used for trading services. The library offers merely models, tests and data and schema generators. The Schemas Generator offers to translate the models to Avro Schemas written in JSON.

## Sponsors
Freya Alpha,
The Kára System,
Spark & Hale Robotic Industries

## TODO
- [ ] Create Default values for enum, array, set, map, etc.

## General
Run and compiled for Python 3.9.13.
Expected to run for Python 3+

## Development

### Testing
run tests with `pytest -s -vv` to see all the details.

### Installation as Consuming Developer

Simply run: `pip install fa-models`

Import in modules without the dash (e.g.): `from famodels.signal import Signal`

### Setup as Contributor
Create the virtul environment: 
```
py -m venv .venv
```
Start the Environment: 
```
./.venv/Scripts/activate
```
 (or allow VS Code to start it). Use `deactivate`to stop it.

All the required libraries must be listed in requirements.txt and installed by  
```
python -m pip install -r .\requirements.txt
```
For Dev use 
```
python -m pip install -r .\requirements-dev.txt
```

To cleanup the environment run:
```
pip3 freeze > to-uninstall.txt
```
 and then
```
pip3 uninstall -y -r to-uninstall.txt
```

or 
```
pip3 install pip-autoremove
```

### Build Library
Prerequisite: make sure that you give your Operating System user the right to modify files in the python directory. The directory where pyhton is installed.
Use `python setup.py bdist_wheel` to create the dist, build and .eggs folder.

## Reference from a different project
In order to use your own version of the project - to maybe contribute to the library - simply clone the code from github into new directory. Then add the path of that new directory to the requirements.txt file of your project. Then change in fa-models whatever you recommend to improve. Don't forget the Open-Closed Principle: extend only (unless it requires a breaking change)


## Releasing a new version

Delete any old files in the /dist and build folder of your local environment.
Update your pip: 
```
python -m pip install --upgrade pip
```

Install the tools build, twine and bumpver: 
```
python -m pip install build twine bumpver
```
Upgrade the setuptools: 

```
pip install --upgrade setuptools
```

Bump the version in pyproject.toml: 
```
bumpver update --patch
```
This will commit a new version to GitHub.

Build the project: 
```
python -m build
```

Check the distribution: 
```
twine check dist/*
```

Upload to test-pypi to validate: 
```
twine upload -r testpypi dist/*
```

Login with username: (password should be known)

If the test-upload was successful, finally, upload to pypi production: 

```
twine upload dist/*
```

Done.

(P.S. Do not forget to update the library in your projects: `pip install --upgrade fa-models`)bumpver update --patch

