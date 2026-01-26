from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
from skill_hub import __version__

setup(
    name="agent-skills-hub",
    version=__version__,
    author="youzaiAGI",
    author_email="youzaiagi@gmail.com",
    description="A package manager for Agent skills",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.1",
        "windows-curses>=2.3.0; sys_platform == 'win32'",
    ],
    entry_points={
        "console_scripts": [
            "skill=skill_hub.__init__:main",
        ],
    },
)
