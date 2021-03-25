# from notebooks.profiles.style_profile import StyleProfile
from pathlib import Path


class PreprocessedText:
    def file(self, file_path: str):
        return open(Path(file_path), "w")


class StyleProfile:
    def feed(self, text: PreprocessedText):
        pass

    def flag(self, text: PreprocessedText) -> bool:
        return True

    def file(self, file_path: str):
        return open(Path(file_path), "w")


class TextProcessor:
    def __call__(self, text: str) -> PreprocessedText:
        return PreprocessedText()


# TODO: Driver
