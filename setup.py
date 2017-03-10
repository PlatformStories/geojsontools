import sys
from setuptools import setup, find_packages

open_kwds = {}
if sys.version_info > (3,):
    open_kwds['encoding'] = 'utf-8'

# with open('README.md', **open_kwds) as f:
#     readme = f.read()

# long_description=readme,

setup(name='geojsontools',
      version='0.0.0',
      description='Functions for manipulating geojsons',
      classifiers=[],
      keywords='',
      author='Nikki Aldeborgh',
      author_email='nikki.aldeborgh@digitalglobe.com',
      url='https://github.com/platformstories/geojsontools',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['geojson >= 1.3.2',
                        'numpy >= 1.12.0',
                        'bumpversion'
                        ]
      )
