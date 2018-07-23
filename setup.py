import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="powerlink2alarm",
    version="0.0.1",
    author="Bertbert",
    author_email="bertbert@pascada.co.uk",
    description="A Python 3 library for the Visonic Powerlink2 alarm system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bertbert72/powerlink2alarm",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)