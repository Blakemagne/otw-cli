from setuptools import setup, find_packages

setup(
    name="otw-cli",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "otw=otw.cli:main"
        ]
    },
    author="Blakemagne",
    description="CLI companion for OverTheWire wargames",
    python_requires=">=3.7",
)
