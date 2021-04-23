from notebooks.profiles import VotingProfile
import pytest
import pandas as pd


class TestVotingProfile:
    author_texts = [
        pd.DataFrame(
            [
                [1.0, 2.0, 3.0],
                [1.2, 2.2, 3.2],
                [1.5, 1.5, 4.4],
                [0.0, 0.2, 0.3],
                [4.4, 3.3, 2.2],
            ]
        )
    ]

    suspect_texts = [
        pd.DataFrame(
            [[2.9, -3.3, 0.0], [1.1, 2.1, 0.0], [-2.0, -5.5, 0.0], [8.3, 9.2, 0.0]],
            index=pd.MultiIndex.from_tuples(
                [(9, 0), (3, 0), (3, 1), (3, 2)], names=["name0", "name69"]
            ),
        ),
    ]

    @pytest.mark.parametrize('author_text, suspect_text', zip(author_texts, suspect_texts))
    def test_voting_profile_should_take_majority_vote(self, author_text, suspect_text):
        profile = VotingProfile(p=0.7)

        profile.feed(author_text)
        distances = profile.distances(suspect_text)
