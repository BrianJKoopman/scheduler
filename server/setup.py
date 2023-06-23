import setuptools

setuptools.setup(
    name="scheduler_server",
    version="0.1.0",
    author="Yilun Guan",
    author_email="yilun.guan@utoronto.ca",
    description="scheduler server",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "scheduler_server": ["config.yaml", "*.txt"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "flask",
        "flask-cors",
        "gunicorn",
        "numpy",
        "pyyaml",
        "pandas",
        #"schedlib @ git+https://github.com/simonsobs/scheduler.git@main",
    ],
)

