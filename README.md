# geojsontools

[![PyPI version](https://badge.fury.io/py/geojsontools.svg)](https://badge.fury.io/py/geojsontools)

A collection of functions for manipulating [geojson](http://geojson.org/) files.


## Installation/Usage

In a virtualenv or conda virtual environment:

```bash
pip install geojsontools
```


## Development

Clone the repo:

```bash
git clone https://github.com/digitalglobe/geojsontools
cd geojsontools
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Please follow [this python style guide](https://google.github.io/styleguide/pyguide.html). 80-90 columns is fine.


### Create a new version

To create a new version:

```bash
bumpversion ( major | minor | patch )
git push --tags
```

Then upload to pypi.
