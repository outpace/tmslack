import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tmslack",
    version="0.0.1.dev",
    author="Daniel Solano Gómez",
    author_email="daniel.solano@outpace.com",
    description="Invite fellow slack users into your tmate session.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/outpace/tmslack",
    license='Apache Software License 2.0',
    packages=setuptools.find_packages(),
    install_requires=[
        'Click >= 7.0',
        'PyYAML >= 3.13',
        'slackclient >= 1.3.0',
        'xdg >= 3.0.2'
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    entry_points={
        'console_scripts': [
            'tmslack = tmslack:main'
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)