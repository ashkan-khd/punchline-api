import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = "0.0.2"
DESCRIPTION = "To be added in the future"


setuptools.setup(
    name="punchline_interfaces",
    version=VERSION,
    author="Ashkan Khademian",
    author_email="ashkan.khd.q@gmail.com",
    description=DESCRIPTION,
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[

    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Framework :: Flask",
        "Framework :: Nameko",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
