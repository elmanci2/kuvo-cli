from setuptools import setup

setup(
    name='kuvo',
    version='1.0.1',
    packages=['app'],
    entry_points={
        'console_scripts': [
            'kuvo=app.kuvo:main',
        ],
    },
    install_requires=[
        'click',
        'tqdm',
        'questionary'
    ],
)
