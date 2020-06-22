import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="funding",
    version="0.0.1",
    author="Carolyn Langen",
    author_email="carolyn@almende.com",
    description="Funding opportunities manager",
    long_description=__doc__,
    url="https://github.com/almende/virtualOfficeManager/tree/master/funding",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = [
        "flask",
        "pytest",
        "flask_cors",
        "gunicorn",
        "flask-restx",
        "pymongo"
    ]
)
