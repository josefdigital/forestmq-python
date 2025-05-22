from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='forestmq',
    version='0.2.1',
    description='Python client for ForestMQ',
    packages=["forestmq"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    py_modules=["flask_jwt_router"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/josefdigital/forestmq-python",
    author="Josef Digital",
    author_email="contact@josef.digital",
    install_requires=[
        "httpx",
    ]
)
