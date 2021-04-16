from notebooks.segmenters import Sentencizer


class TestSentencizer:
    def test_sentencizer_should_split_text_to_sentences(self):
        sentencizer = Sentencizer()

        sentences = sentencizer(
            "There once was a negative boy, who was all mixed up. So he went to a "
            "radical party. But because he was square, he lost out on four awesome "
            "chicks. So he cried his way home, and by the end of the night, it was "
            "2 a.m."
        )

        assert sentences == [
            "There once was a negative boy, who was all mixed up.",
            "So he went to a radical party.",
            "But because he was square, he lost out on four awesome chicks.",
            "So he cried his way home, and by the end of the night, it was 2 a.m.",
        ]
