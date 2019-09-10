#!/usr/bin/env python3
import unittest
from SystemSingleton import SystemSingleton, SystemSingletonException
from subprocess import Popen, check_call, CalledProcessError, DEVNULL
import time

class TestSingleton(SystemSingleton):
    pass

class SingletonTestCase(unittest.TestCase):
    def test_singleton_class(self):
        with TestSingleton() as s1:
            with self.assertRaises(SystemSingletonException):
                with TestSingleton() as s2:
                    pass

    def test_singleton_files(self):
        p1 = Popen(['python3', 'SingletonTest.py'])
        time.sleep(0.2)
        with self.assertRaises(CalledProcessError):
            check_call(['python3', 'SingletonTest.py'], stderr=DEVNULL)
        p1.terminate()
        p1.wait()

if __name__ == '__main__':
    unittest.main()
