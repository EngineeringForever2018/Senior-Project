from setuptools import setup

with open("requirements/common.txt", "r") as req:
    requirements = req.readlines()
    requirements = [requirement.strip() for requirement in requirements]
    requirements = list(filter(lambda s: len(s) > 0, requirements))

setup(
    name="notebooks",
    version="0.0.0",
    packages=[
        "notebooks",
        "notebooks.resources",
        "notebooks.profiles",
        "notebooks.feature_extractors",
        "notebooks.segmentation",
        "notebooks.thresholders",
    ],
    include_package_data=True,
    install_requires=requirements,
    # install_requires=[
    #     "torch",
    #     "tqdm",
    #     "torchtext",
    #     "numpy",
    #     "spacy",
    #     "scipy",
    #     "pandas",
    #     "tables",
    #     "pdpipe"
    #     # 'somepackage==1.2.0',
    #     # 'repo @ https://github.com/user/archive/master.zip#egg=repo-1.0.0',
    #     # 'anotherpackage==4.2.1'
    # ],
)
