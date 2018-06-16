# detail tasks

One of the problems that we've encountered with celery is
that we want to provide the user a lot more information 
about what is happening during the execution of a task
so that they have some sort of visual feedback of 
what is going on in the background.  For customers, this
is extremely helpful because it indicates that their request
is being processed.  For your internal agents / business users,
this is a vital tool to assist in debugging.  To that end,
we've "extended" (ed., wasn't it really hacked into) celery
to provide a `Task` base class that allows you to provide 
much more detail to the user as a task is executing.  That
said, hooking all the pieces together to get this working 
can be a bit overwhelming.  You'll be using the 
following classes and functions for all of this to work:

* **`djenga.celery.tasks.DetailTask`**: Base `Task` class 
  that provides helper functions for adding detailed 
  info for the user  
* **`djenga.celery.tasks.TaskDetail`**: A class that assists 
  in the management of the detail information, used internally only
* **`djenga.celery.backends.RedisDetailBackend`**: A celery 
  backend that ensures the detail information gets saved to 
  redis, when provided by the task
* **`djenga.celery.backends.patch_aliases`**: a function that
  patches the dict of celery aliases to make the `RedisDetailBackend` 
  available to celery with the `redisd` prefix.
* **`djenga.management.commands.debug_celery`**: a management command
  that allows you to run celery using manage.py.  We've found
  this command to be very helpful in debugging celery on windows
  using pycharm.  
* **`djenga.celery.results.AsyncDetailedResult`**: a result class
  that reads the detailed status information from redis and makes
  it available to the caller.  

# setting up your celery app

In your celery app, you will need to add an `__init__` function
that will patch the backends to make the `RedisDetailBackend` 
available.  We need the `RedisDetailBackend` to make sure the
detailed task status gets saved back to redis every time it 
is updated in the task as well as when the task completes or 
errors out.

In the example below, we (1) patch the djenga `RedisDetailBackend`
into celery and (2) set the `DetailTask` class as the default
base task for all tasks.  (2) is completely optional.  You can
still use the regular base `celery.app.Task` class as the base
task and then use `base=DetailTask` when [decorating your task
as discussed in the celery docs](http://docs.celeryproject.org/en/latest/userguide/tasks.html#task-inheritance). 

First, in your settings, make sure to use the `redisd` prefix for 
your `CELERY_RESULT_BACKEND`

e.g.

```python
CELERY_RESULT_BACKEND = 'redisd://127.0.0.1/15'
```

Then, when you define your celery app, use

```python
from celery.app.base import Celery

class MyCeleryApp(Celery):
    def __init__(self, main=None, loader=None, backend=None,
                 amqp=None, events=None, log=None, control=None,
                 set_as_current=True, tasks=None, broker=None, include=None,
                 changes=None, config_source=None, fixups=None, task_cls=None,
                 autofinalize=True, namespace=None, strict_typing=True,
                 **kwargs):
        from djenga.celery.tasks import DetailTask
        from djenga.celery.backends import patch_aliases
        # call patch_aliases to make use of the redis detail backend
        patch_aliases()
        # optional:  set the DetailTask as the default class type for
        # all classes by specifying the `task_cls=DetailTask` below.
        super().__init__(main, loader, backend, amqp, events, log, control,
                         set_as_current, tasks, broker, include, changes,
                         config_source, fixups, task_cls=DetailTask,
                         autofinalize=autofinalize, namespace=namespace,
                         strict_typing=strict_typing, **kwargs)

```

_or, alternatively,_

```python
from celery.app.base import Celery
from djenga.celery.tasks import DetailTask

class MyCeleryApp(Celery):
    def __init__(self, main=None, loader=None, backend=None,
                 amqp=None, events=None, log=None, control=None,
                 set_as_current=True, tasks=None, broker=None, include=None,
                 changes=None, config_source=None, fixups=None, task_cls=None,
                 autofinalize=True, namespace=None, strict_typing=True,
                 **kwargs):
        from djenga.celery.backends import patch_aliases
        # call patch_aliases to make use of the redis detail backend
        patch_aliases()
        # optional:  set the DetailTask as the default class type for
        # all classes by specifying the `task_cls=DetailTask` below.
        super().__init__(main, loader, backend, amqp, events, log, control,
                         set_as_current, tasks, broker, include, changes,
                         config_source, fixups, task_cls=task_cls,
                         autofinalize=autofinalize, namespace=namespace,
                         strict_typing=strict_typing, **kwargs)
                   
                         
app = MyCeleryApp()
@app.task(base=DetailTask)
def my_cool_task():
    print('celery rocks!')
```

# adding detail to your tasks

You can add detail to your tasks using the helper functions
available on the bound task instance:

  * `DetailTask.start_step`
  * `DetailTask.update_step`
  * `DetailTask.end_step`
  
For example,

```python
from djenga_tests.celery import app

@app.task(bind=True, name='gru.steal_the_moon', 
          base='djenga.celery.tasks.DetailTask')
def steal_the_moon(self, gru, moon):
    self.start_step(1, 'Fly to the moon')       
    print('First, we fly to the moon')
    self.update_step(1, 'flying to the moon')
    gru.fly_to_the_moon()
    self.end_step()
    
    self.start_step(2, 'Shrink the moon')
    print('I shrink the moon')
    moon.shrink()
    self.end_step()
    
    self.start_step(3, 'Grab the moon')
    print('I grab the moon')
    gru.grab(moon)
    self.end_step()
    
    self.start_step(4, 'Sit on the toilet')
    print('I sit on the toilet, wait, what?')
    gru.sit_on_the_toilet()
    self.end_step()       
```


An alternative way would be to publish your steps ahead
of time and then use just the keys to demarcate the starting
and ending of steps.


```python
from djenga_tests.celery import app


@app.task(bind=True, name='gru.steal_the_moon', 
          base='djenga.celery.tasks.DetailTask',           
          steps=[(1, 'Fly to the moon'), (2, 'Shrink the moon'), 
                 (3, 'Grab the moon'), (4, 'Sit on the toilet')])
def steal_the_moon(self, gru, moon):
    self.start_step(1)       
    print('First, we fly to the moon')
    self.update_step(1, 'flying to the moon')
    gru.fly_to_the_moon()
    self.end_step()
    
    self.start_step(2)
    print('I shrink the moon')
    moon.shrink()
    self.end_step()
    
    self.start_step(3)
    print('I grab the moon')
    gru.grab(moon)
    self.end_step()
    
    self.start_step(4)
    print('I sit on the toilet, wait, what?')
    gru.sit_on_the_toilet()
    self.end_step()       
```


# monitoring the progress of your task

We use the `djenga.celery.results.AsyncDetailedResult` class to
monitor the progress of `DetailTask`s.  

```
from djenga.celery.results import AsyncDetailedResult
task = steal_the_moon.delay()
result = AsyncDetailedResult(task.id)
result.details()
```


# a note on performance

Obviously, saving every update to redis draws a performance 
penalty for the I/O.  We considered this trade-off to be
worthwhile because the additional detail was meant to be
used in the context of a running task being monitored by
a user from a web page.  Given this context, a millisecond
here or there won't make an earth shattering difference 
to the user.  That said, it's best to avoid using details
for tasks that don't have a user-facing profile, especially
if you have tasks that have to be highly performant.   

# using the debug_celery management task

To use the `debug_celery` management task, we also need to set
the `DJENGA_CELERY_MODULE` setting so that we know which app to
invoke and instantiate the celery worker.  e.g.,

```python
DJENGA_CELERY_MODULE = 'djenga_tests.celery'
```
