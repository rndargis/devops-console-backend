#!/usr/bin/env python3

'''
Setup module
'''

from setuptools import setup, find_packages, Command

import os
import subprocess

def execute(cmd):
    proc = subprocess.run(cmd)
    proc.check_returncode()

class InitCommand(Command):
    description="Initialize and Configure the template"

    user_options = [
        ("name=", None, "Project name"),
        ("desc=", None, "Project description"),
        ("rm-helloworld", "c", "Remove helloworld"),
        ("git-commit", "g", "Commit for me")
    ]

    def initialize_options(self):
        self.name = None
        self.desc = None
        self.rm_helloworld = 0
        self.git_commit = 0

    def finalize_options(self):
        if self.name is None:
            raise Exception("Parameter --name is missing")
        if self.desc is None:
            raise Exception("Parameter --desc is missing")

    def run(self):
        print(" => Initializing the template ...")

        if self.rm_helloworld == 1:
            print("    - Remove helloworld")
            os.remove("svc/apis/helloworld.py")
            os.remove("svc/core/helloworld.py")
            execute(
                [
                    "sed",
                    "-i",
                    "/helloworld/d",
                    "svc/core/core.py",
                    "svc/apiv1.py"
                ]
            )

        print("    - Setting project name and description")
        execute(
            [
                "sed",
                "-i",
                "s/PROJECT_NAME/{}/;s/$PROJECT_DESC/{}/".format(self.name, self.desc),
                "svc/config/default.json"
            ]
        )
        execute(
            [
                "sed",
                "-i",
                "s/'PROJECT_NAME'/'{}'/;s/'PROJECT_DESC'/'{}'/".format(self.name, self.desc),
                "setup.py"
            ]
        )
        execute(
            [
                "sed",
                "-i",
                "s/svc/{}/g".format(self.name),
                "Dockerfile",
                "tests/test_service.py",
                "MANIFEST.in"
            ]
        )

        print("    - Renaming svc module to {}".format(self.name))
        os.rename("svc", self.name)

        if self.git_commit == 1:
            print("    - Commit")
            execute(["git", "add", "."])
            execute(["git", "commit", "-m", "Initialize the service"])

        print("  > done")

class BootstrapCommand(Command):
    description="Bootstrap"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(" => bootstrapping development environment ...")

        execute(["pip", "install", "--user", "-e", "."])

        print("  > done")

setup(
    name='PROJECT_NAME',
    description='PROJECT_DESC',
    url='',
    version='0.0.0',
    python_requires='>=3.7',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'aiohttp[speedups]',
        'aiohttp-swagger',
        'prometheus_async[aiohttp]'
    ],
    extras_require={
        'dev': [
            'pylint',
            'pytest-cov',
            'bumpversion',
        ],
        'prod': [
            'gunicorn',
        ],
    },
    test_suite="tests",
    include_package_data=True,

    # Metadata
    author='',
    author_email='',
    license='',
    long_description=open('README.rst').read(),
    keywords=[],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match 'license' above)
        'License :: OSI Approved :: Apache Software License',

        'Operating System :: OS Independent',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # Custom command
    cmdclass={
        'init': InitCommand,
        'bootstrap': BootstrapCommand,
    },
)
