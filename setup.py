import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("pyIslam/__init__.py", "r", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

with open("README.md", "rb") as f:
    readme = f.read().decode("utf-8")

setup(
    name="islam",
    version=version,
    description="a library to calculate prayer times, hijri date, qiblah direction and more",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/abougouffa/pyIslam",
    author="abougouffa",
    author_email="abougouffa@fedoraproject.org",
    license="GPL3+",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="prayer times, hijri date, qiblah direction",
    include_package_data=True,
    packages=["pyIslam"],
)
