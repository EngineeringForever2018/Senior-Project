from setuptools import setup


def convert_requirement(requirement, number):
    if requirement.startswith("https://github.com"):
        return f"en_core_web_sm @ {requirement}"

    return requirement


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
        "notebooks.structures",
    ],
    include_package_data=True,
    install_requires=[
        "torchtext",
        "tqdm",
        "numpy",
        "spacy",
        "scipy",
        "pandas",
        "tables",
        "pdpipe",
        "nltk",
        "sklearn",
        "docx",
        "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0-py3-none-any.whl",
        ],
    # dependency_links=[
    #     (
    #         "https://github.com/explosion/spacy-models/releases/download/"
    #         "en_core_web_sm-3.0.0/en_core_web_sm-3.0.0-py3-none-any.whl"
    #         "#egg=en_core_web_sm"
    #     ),
    # ],
    # install_requires=requirements,
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
