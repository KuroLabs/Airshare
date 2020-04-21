import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="Airshare",
    version="0.0.2",
    author="Kandavel A, Mohanasundar M, Nanda H Krishna",
    author_email="kurolabs.org+airshare@gmail.com",
    description="An easy way to share content in a local network.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KuroLabs/airshare",
    entry_points = {
        'console_scripts': ['airshare=airshare.cli:main'],
    },
    packages=[
        "airshare",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    install_requires=[
        "aiohttp >= 3.6.2",
        "asyncio >= 3.4.3",
        "humanize >= 0.5.1",
        "python-magic >= 0.4.15",
        "pyqrcode >= 1.2.1",
        "requests >= 2.20.0",
        "zeroconf >= 0.25.0",
        "tqdm >= 4.36.1",
        "pyperclip >= 1.8.0",
        "click >= 7.0" ,
    ],
    python_requires='>=3.6',
)
