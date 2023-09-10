from setuptools import setup, find_packages

setup(
    name='Project_X',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Зависимости вашего проекта, если они есть
    ],
    entry_points={
        'console_scripts': [
            'mycommand = project_x.menu:main',
        ],
    },
)