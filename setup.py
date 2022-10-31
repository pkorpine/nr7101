from setuptools import setup
from nr7101.version import __version__

setup(
    name="nr7101",
    version=__version__,
    description="Zyxel NR7101 tool",
    author="Pekka Korpinen",
    author_email="pekka.korpinen@iki.fi",
    license="MIT",
    url="https://github.com/pkorpine/nr7101",
    packages=["nr7101"],
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": ["nr7101-tool=nr7101.cli:cli"],
    },
)
