"""
this setup will check for dependencies and install PhyBio on your computer
"""
from setuptools import setup, find_packages

setup(
    name = "regrets-collector",
    version = "1.0.0",
    url = "https://gitlab.com/phydev/pybot-exec.git",
    author = "duckDev",
    author_email = "mmsoares@uc.pt",
    description = "pythonic bot",
    license = "GNU GPLv3",
    platform = "Python 3.7.2",
    packages = find_packages(),
    install_requires = ["tweepy >= 3.8.0", "numpy >= 1.16.2", "matplotlib >= 3.0.3"],
)
