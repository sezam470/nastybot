from setuptools import setup, find_packages

setup(
    name='nastybot',
    version='0.1.0',
    description='A Telegram bot for developer tasks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Nasty Developer',
    author_email='sezam470@gmail.com',
    url='https://github.com/sezam470/nastybot',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'telebot',
        'gigachat',
        'setuptools'
    ],
    entry_points={
        'console_scripts': [
            'nastybot = nastybot',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: None License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
