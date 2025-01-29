from setuptools import setup, find_packages

setup(
    # Library name and version
    name="odoo_api_manager",
    version="0.2.3",
    
    # Dependencies
    install_requires=[
        "pandas",
    ],

    # My name here
    author="Pável Hernández",
    # Feel free to email me
    author_email="onnymm@outlook.com",

    # Library description
    description="Librería para el manejo de la API de Odoo",

    # Documentation
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/onnymm/odoo_api_manager",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    packages=find_packages(),
)