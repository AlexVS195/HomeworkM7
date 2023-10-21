from setuptools import setup, find_namespace_packages

setup(
    name='clean-folder',
    version='1.0.0',
    author='Oleksandr Symashkin',
    author_email='asemashk@ukr.net',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean=clean-folder.clean:start']}
)