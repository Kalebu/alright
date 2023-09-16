from os import path
from setuptools import setup

# read the contents of your description file

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="alright",
    version="2.61",
    description="Python wrapper for WhatsApp web based on selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kalebu/alright",
    download_url="https://github.com/Kalebu/alright/archive/refs/tags/v1.7.tar.gz",
    author="Jordan Kalebu",
    author_email="isaackeinstein@gmail.com",
    license="MIT",
    packages=["alright"],
    keywords=[
        "alright",
        "python-whatsapp",
        "PyWhatsApp",
        "pywhatsapp",
        "python-whatsapp-wrapper",
    ],
    install_requires=[
        "platformdirs",
        "selenium",
        "webdriver-manager",
    ],
    include_package_data=False,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
