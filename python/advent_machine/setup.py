import os
from setuptools import setup, find_packages, Command

class CleanCmd(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')
        os.system('find . -name "*.pyc" -delete')

setup(
    name='advent_machine',
    version='0.0.1',
    author='Nigel Butt',
    packages=find_packages(exclude=('test')),
    test_suite='test',
    cmdclass={'clean': CleanCmd}
)
