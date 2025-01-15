#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="linux_system_metrics",
    version="1.0.0",
    description="Программа для мониторинга системных метрик",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AnnLinnden",
    packages=find_packages(),
    install_requires=[
        "PyQt5",
        "psutil",
        "matplotlib"
    ],
    entry_points={
        "console_scripts": [
            "linux_system_metrics = linux_system_metrics.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        "": ["*.png"],
    },
)