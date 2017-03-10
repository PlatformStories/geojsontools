# geojsontools

A collection of functions for manipulating [geojsons](http://geojson.org/).

## Installation/Usage

For Ubuntu, install conda with the following commands (choose default options at prompt):

```bash
wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
bash Miniconda2-latest-Linux-x86_64.sh
```

For OS X, install conda with the following commands (choose default options at prompt):

```bash
wget https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh
bash Miniconda2-latest-MacOSX-x86_64.sh
```

Then run:

```bash
bash
```

so that modifications in your .bashrc take effect.

Create a conda environment:

```bash
conda create -n env python ipython numpy
```

Activate the environment:

```bash
source activate env
```

Upgrade pip (if required):

```bash
pip install pip --upgrade
```

Install geojsontools:

```bash
pip install geojsontools
```

Optional: you can install the current version of the master branch with:

```bash
pip install git+https://github.com/platformstories/geojsontools
```

Keep in mind that the master branch is constantly under development.


## Development

Activate the conda environment:

```bash
source activate env
```

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

To exit your conda virtual environment:

```bash
source deactivate
```

### Create a new version

To create a new version:

```bash
bumpversion ( major | minor | patch )
git push --tags
```

Then upload to pypi.
