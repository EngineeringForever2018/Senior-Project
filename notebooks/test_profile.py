from notebooks import StyleProfile, TextProcessor


def test_profile():
    my_first_essay = "a good essay"
    my_second_essay = "a bad essay"

    text_processor = TextProcessor()

    my_first_essay = text_processor(my_first_essay)
    my_second_essay = text_processor(my_second_essay)

    my_profile = StyleProfile()

    my_profile.feed(my_first_essay)

    assert my_profile.flag(my_second_essay) is False
