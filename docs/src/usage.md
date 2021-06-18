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

## Sessions

PyCamunda supports persisting certain parameters like credentials or headers by using 
`requests.session.Session` between different requests. This is done by setting the `session` 
attribute of any request object. 

```python
import requests.auth
import requests.sessions
import pycamunda.processinst

url = "http://localhost:8080/engine-rest"

session = requests.sessions.Session()
session.auth = requests.auth.HTTPBasicAuth(username="demo", password="demo")

get_instances = pycamunda.processinst.GetList(url)
get_instances.session = session
instances = get_instances()
```
Please note that PyCamunda will not update the instance of `Session` in any way. So when for example
the `auth` attribute of the request object is set as well, PyCamunda will use the set `auth` 
attribute of the request object and will not update the session object.

## Advanced
Each class that represents a Camunda endpoint inherits from `pycamunda.base.CamundaRequest`. That 
base class provides functionality that can be helpful for understanding and debugging purposes.

### Request Url
The url for each request can be accessed using the `url` property. The url does often depend on some
id parameter. In some cases the structure of the url can be even more different:

````python
import pycamunda.processdef

url = 'http://localhost:8080/engine-rest'

if __name__ == '__main__':
    start_instance = pycamunda.processdef.StartInstance(url=url, id_='174cb832-a8a7')
    print(start_instance.url)
    start_instance = pycamunda.processdef.StartInstance(url=url, key='MyProcess')
    print(start_instance.url)
````
Output:
```console
http://localhost:8080/engine-rest/process-definition/174cb832-a8a7/start
http://localhost:8080/engine-rest/process-definition/key/MyProcess/start
```

### Request parameters
Each parameter in the request classes is available as a descriptor. That means the parameter can 
always be get and set using attributes:

```python
import pycamunda.user

url = 'http://localhost:8080/engine-rest'

get_users = pycamunda.user.GetList(url=url, first_name='John')
print(get_users.first_name, get_users.last_name)
get_users.last_name = 'Doe'
print(get_users.first_name, get_users.last_name)
```
Output:
```console
John None
John Doe
```
The value that is set needs to be JSON-serializable. Datetime objects are automatically converted
to the isoformat-datetime-string Camunda expects. In case of Enumerations their value is used.

In some cases where the parameter is set using a method instead of providing it in the constructor 
this can be be problematic because the parameter might expect a specific data type (e.g. list or 
dict). Ignoring this will most likely lead to problems when the request is sent.

The parameters sent with the request can be introspected using the `query_parameters()` and
`body_parameters()` methods:
```python
import pycamunda.user

url = 'http://localhost:8080/engine-rest'

create_user = pycamunda.user.Create(
    url=url, id_='johndoe', first_name='John', last_name='Doe', password='changeme'
)
print(create_user.body_parameters())
```
Output:
```console
{
    'profile': {
        'id': 'johndoe', 
        'firstName': 'John', 
        'lastName': 'Doe'
    }, 
    'credentials': {
        'password': 'changeme'
    }
}
```
In some cases files are attached to the request. Those can be introspected with the`file` property.
