import os

from setuptools import find_packages, setup

readme = open("README.md").read()
history = open("CHANGES.md").read()

requirements = open("requirements.txt").read()

docs_require = [
    "Sphinx>=2.2",
    "sphinx_copybutton",
    "sphinx.ext.todo",
    "sphinx_rtd_theme",
    "sphinx_tabs.tabs",
    "sphinx_click"
]

tests_require = [
    "pytest==6.1.1"
]

extras_require = {
}
extras_require["all"] = [req for exts, reqs in extras_require.items() for req in reqs]

setup_requires = [
    "pytest-runner>=5.2",
]

install_requires = requirements

packages = find_packages()

g = {}
with open(os.path.join("sitscwl", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name="sitscwl",
    version=version,
    description=__doc__,
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    keywords=["Satellite Image Time Series", "Big EO", "Data Cubes"],
    license="MIT",
    author="Felipe Menino Carlos",
    author_email="efelipecarlos@gmail.com",
    url="https://github.com/M3nin0/sitscwl",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Console :: Curses  ",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
