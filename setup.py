from setuptools import setup, find_packages


setup(
    name='slimpoint',
    version='1.0.4',
    description='Slim, readable, expressive interactions with backend services',
    author='Brandon Blair',
    author_email='cbrandon.blair@gmail.com',
    url='https://github.com/brandonblair/slimpoint',
    packages=find_packages(),
    install_requires=["requests>=2.18.4"]
)