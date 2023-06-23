from setuptools import find_packages, setup

setup(
    name="schedlib",
    version="0.1.0",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),    
    install_requires=[
        "toolz",
        "pandas",
        "chex",
        "pyephem",
        "typing-extensions",
    ],
)
