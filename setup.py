from setuptools import setup, find_packages

setup(
    name="echolight",
    version="0.1.0",
    author="Anthony Grimes",
    author_email="echolight@raynes.me",
    include_package_data=True,
    url="https://github.com/Raynes/echolight",
    install_requires=[
        'phue==0.8',
        'flask==0.10.1'
    ],
    packages=find_packages()
)
