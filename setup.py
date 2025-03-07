from setuptools import setup, find_packages

setup(
    name='translator_subs',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'googletrans==4.0.0-rc1',
        'deepl',                  
        'tqdm'                     
    ],
    entry_points={
        'console_scripts': [
            'translator-subs=translate:main',
        ],
    },
    author='URRSSS23',
    author_email='freecpstr.com',
    description='An automatic translator for ASS/SSA subtitles',
    url='https://github.com/URRSSS23/Translator_subs',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
