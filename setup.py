from setuptools import setup, find_packages

setup(
    name="odoo_api_manager",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pandas==2.2.2", "numpy==2.0.0"],
    author="Pável Hernández",
    author_email="onnymm@outlook.com",
    description="Librería para el manejo de la API de Odoo",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/onnymm/odoo_api_manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)