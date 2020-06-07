[![Build Status](https://travis-ci.com/pklauke/pycamunda.svg?branch=master)](https://travis-ci.com/pklauke/pycamunda)
[![codecov](https://codecov.io/gh/pklauke/pycamunda/branch/master/graph/badge.svg)](https://codecov.io/gh/pklauke/pycamunda)
[![Documentation Status](https://readthedocs.org/projects/pycamunda/badge/?version=latest)](https://pycamunda.readthedocs.io/en/latest/?badge=latest)

# PyCamunda
A high-level framework for communicating with the workflow and decision automation engine Camunda. 

PyCamunda supports following Camunda REST api resources:
  * Deployment
  * External Task
  * Filter
  * Group
  * Incident
  * Message
  * Process Definition (excluding form endpoints)
  * Process Instance (Delete, GetActivityInstance, GetList, Get, Modify, ActivateSuspend)
  * Signal 
  * Task (excluding subresources)
  * User
  * Variable Instance

## Installation

PyCamunda can be installed from the offical <a href="https://pypi.org">Python Package Index</a>.

```
$ pip install pycamunda
```

## Documentation

The latest documentation can be found <a href="https://pycamunda.readthedocs.io/en/latest/index.html">here</a>.
