from SystemSingleton import SystemSingleton
import time

class SingletonTest(SystemSingleton):
    def __init__(self):
        super().__init__(runfile_path='.')

    def run(self):
        time.sleep(10)

if __name__ == '__main__':
    with SingletonTest() as s:
        s.run()
