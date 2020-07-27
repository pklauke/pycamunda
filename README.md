[![Build Status](https://travis-ci.com/pklauke/pycamunda.svg?branch=master)](https://travis-ci.com/pklauke/pycamunda)
[![codecov](https://codecov.io/gh/pklauke/pycamunda/branch/master/graph/badge.svg)](https://codecov.io/gh/pklauke/pycamunda)
[![Documentation Status](https://readthedocs.org/projects/pycamunda/badge/?version=latest)](https://pycamunda.readthedocs.io/en/latest/?badge=latest)

# PyCamunda
PyCamunda is a Python REST api client for the workflow and decision automation engine Camunda. 

PyCamunda takes care of Camunda-specific characteristics and gives you an intuitive Python interface so you can focus on developing your actual business application. So PyCamunda deals with http requests, nested dictionaries, camelCase keys,  datetime formatting and more for you.

Simply..
* .. create an instance of the PyCamunda class corresponding to a Camunda endpoint,
* .. configure it using keyword arguments and methods,
* .. send the request and get the response serialized in a Python data class.

```python
import pycamunda.processinst

url = 'http://localhost/engine-rest'

get_instances = pycamunda.processinst.GetList(url, process_definition_key='MyProcess')
instances = get_instances()

for instance in instances:
    print('Process instance id:', instance.id_)
```
Output:
```console
Process instance id: 174cb832-a8a7-11ea-8129-0242ac110002
Process instance id: 1a70a8e9-a7ed-11ea-8129-0242ac110002
...
```

## Installation

PyCamunda requires Python >= 3.7 and can be installed from the offical <a href="https://pypi.org">Python Package Index</a>.

```
$ pip install pycamunda
```

## Documentation

The latest documentation can be found <a href="https://pycamunda.readthedocs.io/en/latest/index.html">here</a>.
