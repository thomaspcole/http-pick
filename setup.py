import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="http_pick",
    version="0.1",
    author="Thomas Cole",
    author_email="thomas.patrick.cole@gmail.com",
    description="A http/https handler that lets you pick the web browser you want to use.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thomaspcole/http-pick",
    project_urls={
        "Bug Tracker": "https://github.com/thomaspcole/http-pick/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'PyQt5',
        'pynput'
    ],
    python_requires=">=3.6",
    entry_points={  
        'console_scripts': [
            'http-pick=http_pick.launcher:main',
        ],
    },
    data_files=[
        ('share/applications', ['HTTP-Pick.desktop'])
    ]
)