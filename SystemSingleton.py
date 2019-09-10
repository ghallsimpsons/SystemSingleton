import os
import subprocess

class SystemSingletonException(Exception):
    pass

class SystemSingleton(object):
    """
    Allow only a single instance of a class to exist.

    >>> class MyClass(SystemSingleton):
    ...     pass
    >>> with MyClass() as my_class:
    ...     # Only one instance can run
    ...     my_class.do_thing()
    """

    def __init__(self, runfile_path='.'):
        # Allow users to change runfile location
        self.runfile_path = runfile_path

    def __enter__(self):
        self.get_process_lock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.free_process_lock()

    @property
    def pid_filename(self):
        """
        Use DerivedClass.pid as PID file.
        """
        fname = ".{cls}.pid".format(cls=self.__class__.__name__)
        if hasattr(self, "runfile_path"):
            return os.path.join(self.runfile_path, fname)
        else:
            return fname

    def get_process_lock(self):
        """
        Check if PID file is empty, and if so, add our PID and start time so
        another process can not run. If the PID file is not empty, check if the
        PID corresponds to a process started at the same time. If so,
        get_process_lock raises a SystemSingletonException.
        """
        try:
            with open(self.pid_filename, 'r') as lock_file:
                pid, start_time = lock_file.read().strip().split(',')
        except (IOError, ValueError):
            # No pid file existed, or was empty. That's fine.
            pass
        else:
            # If PID file did exist, we check if it corresponds to a running process.
            if start_time == self.__process_start_time(pid):
                raise SystemSingletonException("Process already running: PID {0}".format(pid))

        # Get the lock
        with open(self.pid_filename, 'w+') as lock_file:
            my_start_time = self.__process_start_time(os.getpid())
            lock_file.write("{pid},{start_time}".format(pid=os.getpid(),
                    start_time=my_start_time))

    def free_process_lock(self):
        """
        Clear PID file so another process can start.
        """
        with open(self.pid_filename, 'w+') as lock_file:
            pass

    @staticmethod
    def __process_start_time(pid):
        """
        Returns start time of process
        """
        if not(isinstance(pid, int) or pid.isdigit()):
            return None
        try:
            return subprocess.check_output(
                ["ps", "--no-headers", "-o", "lstart", "-p", str(pid)]
                ).decode().strip()
        except subprocess.CalledProcessError:
            return None
