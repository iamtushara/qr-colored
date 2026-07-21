"""
Once the project is set-up, run the following command on the console
to make use of the entry-points:
>>> pip install -e .

This will enable user to run the module from the command line
following way:
>>> qr-colored
"""

# type: ignore
# pylint: skip-file

from setuptools import find_packages, setup
import versioneer


requirements = [
    # package requirements (other than Python) go here
    # add required dependencies that are also specified in environment.yml

]

setup(
    name='qr-colored',
    # version=versioneer.get_version(),
    packages=find_packages(where='.', exclude=['tests', 'tests.*']),
    install_requires=requirements,
    keywords='qr-colored',
    classifiers=[
        'Programming Language :: Python :: 3.13',
    ],
    entry_points={
        'console_scripts': [
            'qr-colored = qr_colored.cli:main'
        ]
    }
)
