from setuptools import setup, find_packages

setup(
    name="django-email-sender",
    version="1.10",
    packages=find_packages(),
    install_requires=[
        "Django>=3.2,<6.0",
    ],
    author="Egbie Uku",
    author_email="egbieuku@hotmail.com",
    description="A chainable Django email sender utility.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/EgbieAndersonUku1/django-email-sender",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 5.0",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    
)


