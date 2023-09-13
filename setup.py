from setuptools import setup, find_packages

setup(
    name='NoteBook_Buddy',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        #требования
    ],
    entry_points={
        'console_scripts': [
            'startbuddy = NoteBook_Buddy.menu:main',
        ],
    },
)