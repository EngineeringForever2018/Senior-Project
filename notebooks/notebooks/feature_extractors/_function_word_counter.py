from notebooks.feature_extractors import BaseSegmentExtractor
from pkg_resources import resource_stream
from typing import List


# TODO: Tests
class FunctionWordCounter(BaseSegmentExtractor):
    def __init__(self):
        with (resource_stream("notebooks.resources", "filtered_function_words.txt")) as f:
            data = f.read().decode("utf-8")
            self._words = list(filter(lambda s: len(s) > 0, data.split(sep="\n")))

    def _segment_extract(self, segment: str) -> List[float]:
        counts = []

        for word in self._words:
            normal_count = segment.count(" " + word + " ")
            punct_word = segment.count(" " + word + ",")
            start_word = segment.count(word.capitalize() + " ")
            end_word = segment.count(" " + word + ".")

            counts.append(float(normal_count + punct_word + start_word + end_word))

        return counts
