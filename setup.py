import sys
import setuptools

sys.path.insert(0, 'src')
from coffee.mqtt import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
test_requirements = ['pytest']
test_setup_requires = ['pytest-runner']

setuptools.setup(
    name='coffee-mqtt',
    version=__version__,
    description="Python MQTT framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alessio Volpe",
    author_email="alessio.volpe@aol.com",
    url="https://github.com/phocs/coffee-mqtt",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    license='MIT License Copyright (c) 2020 Alessio Volpe',
    keywords='coffee',
    classifiers=[
        'License :: OSI Approved',
        'Natural Language :: English',
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'Topic :: Communications',
        'Topic :: Internet',
    ],
    python_requires='>=3.6',
    test_suite='tests',
    setup_requires=test_setup_requires,
    tests_require=test_requirements,
)
