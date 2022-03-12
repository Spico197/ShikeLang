import os
import setuptools

from shikelang import __version__


readme_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
with open(readme_filepath, "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="shikelang",
    version=__version__,
    author="Tong Zhu",
    author_email="tzhu1997@outlook.com",
    description="Bon Appétit 💩",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/Spico197/ShikeLang",
    packages=setuptools.find_packages(exclude=["tests", "tests.*", "docs", "docs.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],
    include_package_data=True,
    entry_points={"console_scripts": ["skl = shikelang.cmd:main"]},
)
