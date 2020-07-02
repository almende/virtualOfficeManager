import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="show_and_tell",
    version="0.0.1",
    author="Carolyn Langen",
    author_email="carolyn@almende.com",
    description="Show and tell manager",
    long_description=__doc__,
    url="https://github.com/almende/virtualOfficeManager/tree/master/show_and_tell",
    packages=setuptools.find_packages(include=['flaskr', 'flaskr.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = [
        "flask",
        "pytest",
        # "authlib==0.13",
        "google-api-python-client",
        # "google-auth",
        # "virtualenv",
        "oauth2client",
        "flask_cors",
        "waitress",
        "flask-restx"
    ]
)
