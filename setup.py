import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ttcnotify',  
    version='0.1',
    scripts=['ttcnotify/TTCNotify'],
    author="Merlin Roe",
    description="Monitoring tool for Tamriel Trade Centre auction house, in Elder Scrolls Online",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MerlinR/TTCNotifier",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )
