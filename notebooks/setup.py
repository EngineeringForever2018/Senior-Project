from setuptools import setup

setup(
    name='notebooks',
    version='0.0.0',
    packages=['notebooks',
              'notebooks.resources',
              'notebooks.profiles',
              'notebooks.nets',
              'notebooks.feature_extractors',
              'notebooks.datatools'],
    include_package_data=True,
    install_requires=[
        'torch',
        'tqdm',
        'torchtext',
        'numpy',
        'spacy',
        'scipy',
        'pandas',
        'tables',
        'pdpipe'
        # 'somepackage==1.2.0',
        # 'repo @ https://github.com/user/archive/master.zip#egg=repo-1.0.0',
        # 'anotherpackage==4.2.1'
    ],
)