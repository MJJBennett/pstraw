import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pstraw",
    version="0.0.5",
    author="Michael Bennett",
    author_email="michaelbennett.dev@gmail.com",
    description="A very light wrapper for the Strawpoll API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MJJBennett/pstraw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
