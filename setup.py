from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='jupi',
    version='0.1',
    description='Jenkings USB Power Indicator',
    long_description=readme(),
    keywords='jenkins usb',
    url='https://github.com/thomasrynne/jupi',
    author='Thomas Rynne',
    author_email='jupi@thomasrynne.co.uk',
    license='GPLv3',
    packages=['jupi'],
    include_package_data=True,
    install_requires=[
        'jenkinsapi','pyusb','websocket-client'
    ],
    zip_safe=False,
    platforms=["linux"],
    entry_points = {
        'console_scripts': ['jupi=jupi:main'],
    })
