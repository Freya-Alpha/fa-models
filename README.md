# fa-models
A set of models often used for trading services. The library offers no algorithms - just models.

## General
Run and compiled for Python 3.9.13.

## Development


### Installation as Consuming Developer

Simply run:

`pip install fa-models`

### Setup as Contributor
Create the virtul environment: `py -m venv .venv`
Start the Environment: `./.venv/Scripts/activate`. Use `deactivate`to stop it.
Update the PIP: `py -m pip install --upgrade pip`

All the required libraries must be listed in requirements.txt and installed by  `py -m pip install -r .\requirements.txt`

To cleanup the environment run:
`pip3 freeze > to-uninstall.txt` and then
`pip3 uninstall -y -r to-uninstall.txt`

or `pip3 install pip-autoremove`

### Build Library
Preqrequisite: make sure that you give your Operating System user the right to modify files in the python directory. The directory where pyhton is installed.
Use `python setup.py bdist_wheel` to create the dist, build and .eggs folder.

## Reference from a different project
In order to use your own version of the project - to maybe contribute to the library - simply clone the code from github into new directory. Then add the path of that new directory to the requirements.txt file of your project. Then change in fa-models whatever you recommend to improve. Don't forget the Open-Closed Principle: extend only (unless it requires a breaking change)


### Releasing a new version

Install the tools build and twine: python -m pip install build twine`

Delete any old files in the /dist folder.

Bump the version in pyproject.toml.

Build the project: `python -m build`

Check the distribution: `twine check dist/*`

Upload to test-pypi to validate: `twine upload -r testpypi dist/*`

Login with username: svabra (password should be known)

Finally, upload to pypi production: `twine upload dist/*`

