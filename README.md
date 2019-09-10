# SystemSingleton

A simple base class which allows only a single instance of derived classes to
exist on the system at a given time (relies on `pgrep`).

## Usage

Critical singleton methods can be protected by calling them from within a `with`
block.

```python3
class MyClass(SystemSingleton):
    def __init__(self):
        pass

    def critical_function(self):
        pass

with MyClass() as me:
    me.critical_function()
```

This will allow only a single instance of `MyClass` to run `critical_function`
at once. It does this by creating a `.MyClass.pid` file in the current working
directory with the PID and start time of the process. To change the location
of the PID file, you can provide a directory to the base class:

```python3
class MyClass(SystemSingleton):
    def __init__(self):
        super().__init__(runfile_path='/var/run')
```

## Design Principles

`SystemSingleton` was designed with cron jobs in mind, meant to mindlessly
prevent overlapping jobs. Two other important principles were: 1) it must be
easy to shove into existing code, and 2) it should still allow you to
interactively create and work with wrapped classes if mutex operation is not
needed. For instance, you ought to be able to do the following:

```python3
# Process 1
with MyClass() as me:
    me.critical_function()

# Process 2
me = MyClass()
me.auxiliary_function()
```

Additionally, since such jobs are often unmonitored, it should gracefully
handle both process crashes and system crashes. It also should not rely on
any particular permissions, which precludes reliance on e.g. a `tmpfs` lockfile
solution. This motivated the implementation of the PID file format.

## Pitfalls

If a global runfile path is not provided, instances launched from different
working directories will run simultaneously.

The runfile is not checked and written atomically. If two processes are started simultaneously, both are likely to run.

