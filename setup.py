from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='Bot_Anders',
    version='0.10',
    install_requires=requirements,
    packages=['bot', 'bot.commands', 'bot.strawpoll_api', 'minesweeper'],
    url='https://github.com/PatrickSchmitt98/Bot_Anders',
    license='MIT',
    author='Patrick Schmitt',
    author_email='patrick_98@t-online.de',
    description='A simple discord bot',
    long_description=long_description
)
