import os.path
import setuptools


def read(name):
    mydir = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(mydir, name)).read()


setuptools.setup(
    name="mkdocs-diagrams",
    version="0.0.1",
    packages=["mkdocs_diagrams"],
    url="https://github.com/zoni/mkdocs-diagrams",
    license="MIT",
    author="Nick Groenen",
    author_email="nick@groenen.me",
    description="MkDocs plugin to render Diagrams files",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    install_requires=["mkdocs"],
    entry_points={"mkdocs.plugins": ["diagrams = mkdocs_diagrams:DiagramsPlugin",]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)