import setuptools
import sys

with open("PIP.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="Airshare",
    version="0.1.1",
    author="Kandavel A, Mohanasundar M, Nanda H Krishna",
    author_email="kurolabs.org+airshare@gmail.com",
    description="An easy way to share content in a local network.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KuroLabs/airshare",
    entry_points={
        "console_scripts": ["airshare=airshare.cli:main"],
    },
    packages=[
        "airshare",
    ],
    include_package_data=True,
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
    ],
    install_requires=[
        "aiohttp >= 3.6.2",
        "asyncio >= 3.4.3",
        "click >= 7.0",
        "humanize >= 0.5.1",
        "pyperclip >= 1.8.0",
        "pyqrcode >= 1.2.1",
        "requests >= 2.20.0",
        "requests-toolbelt >= 0.9.1",
        "tqdm >= 4.36.1",
        "zeroconf >= 0.25.0",
    ],
    python_requires=">=3.6",
)
