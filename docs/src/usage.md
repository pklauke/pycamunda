# Usage

For each Camunda REST api endpoint PyCamunda offers classes for sending requests. Responses are 
serialized and returned in dataclasses. Each PyCamunda module represents one Camunda REST api 
resource. 

## Starting a process instance

The [processdef](processdef) module provides classes to interact with process definitions. To start 
an instance of a definition the class `StartInstance` is used. The process definition is specified 
by the `key` argument using the process definition key. Alternatively the `id_` argument could be 
used for the process definition id. To start the process instance with initial variables they are 
added using the respective method. Finally, the process instance is started by calling the object. 

```python
import pycamunda.processdef


url = 'http://localhost/engine-rest'

start_instance = pycamunda.processdef.StartInstance(url=url, key='MyProcessDefinition')
start_instance.add_variable(name='InitVariable', value=1)
process_instance = start_instance()
```


## Fetching and completing external service tasks

The [externaltask](externaltask) module provides classes to interact with external service tasks. 
Those can be fetched using the class `FetchAndLock`. Service task topics that want to be fetched are
 added to the object. If variables of the process instance are needed to complete the task, those 
 can be requested from the process instance when adding the topic.

To complete a task the class `Complete` is used. Variables that want to be added to the process 
instance are added to that class.

```python
import pycamunda.externaltask

url = 'http://localhost/engine-rest'
worker_id = 'my-worker'
variables = ['InitVariable']  # variables of the process instance


fetch_and_lock = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
fetch_and_lock.add_topic(name='MyServiceTaskTopic', lock_duration=10000, variables=variables)
tasks = fetch_and_lock()

for task in tasks:
    complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)
    complete.add_variable(name='ServiceTaskVariable', value=2)  # Send this variable to the instance
    complete()
```

## Authentication

In case authentication for the REST api of Camunda is enabled as described in
<a href="https://docs.camunda.org/manual/latest/reference/rest/overview/authentication/">Configure Authentication</a>,
base64-encoded credentials have to be provided with each request. In PyCamunda this can be done
by using the `auth` attribute.
```python
import requests.auth
import pycamunda.task


url = 'http://localhost:8080/engine-rest'

get_tasks = pycamunda.task.GetList(url)
get_tasks.auth = requests.auth.HTTPBasicAuth(username='demo', password='demo')
tasks = get_tasks()
```
PyCamunda will raise a `pycamunda.Unauthorized` exception if the authentication fails.
