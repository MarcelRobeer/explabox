"""Character-level perturbations."""

import warnings

from text_sensitivity.perturbation import (add_typos, delete_random,
                                           random_case_swap, random_lower,
                                           random_spaces, random_upper,
                                           swap_random)


def random_string(n: int = 10, min_length: int = 10, max_length: int = 100, special_characters=None):
    """Generate random strings.

    Args:
        n (int, optional): Amount of generated strings. Defaults to 10.
        min_length (int, optional): Minimum length of a string. Defaults to 10.
        max_length (int, optional): Maximum length of a string. Defaults to 100.
        special_characters: List of special characters that will be used in the strings.
            Choose from "ascii", "emojis", "whitespace", "ascii_upper", "ascii_lower", "digits", "punctuation",
            "cyrillic" and "all". "all" uses all the special characters before. Defaults to None.

    Returns:
        List of random strings
    """
    if special_characters is None:
        special_characters = []
    if isinstance(special_characters, str):
        special_characters = [special_characters]

    from text_sensitivity import (RandomAscii, RandomCyrillic, RandomDigits,
                                  RandomEmojis, RandomLower, RandomPunctuation,
                                  RandomSpaces, RandomUpper, RandomWhitespace)

    generator_set = set()
    warnings.simplefilter("always", UserWarning)
    special_character_dict = {
        "ascii": RandomAscii(),
        "emojis": RandomEmojis(),
        "whitespaces": RandomWhitespace(),
        "spaces": RandomSpaces(),
        "ascii_upper": RandomUpper(),
        "acii_lower": RandomLower(),
        "digits": RandomDigits(),
        "punctuation": RandomPunctuation(),
        "cyrillic": RandomCyrillic(),
    }
    for special_character in special_characters:
        if special_character == "all":
            for character in special_character_dict.values():
                generator_set.add(character)
        elif special_character in special_character_dict:
            generator_set.add(special_character_dict[special_character])
        else:
            warnings.warn(
                f'Unknown special_character "{special_character}". Skipping to next one.',
                f'Possible special characters are: all, {", ".join(list(special_character_dict.keys()))}.',
            )
    if generator_set:
        from text_sensitivity import combine_generators

        return combine_generators(*list(generator_set)).generate_list(n=n, min_length=min_length, max_length=max_length)

    from text_sensitivity import RandomString

    return RandomString().generate_list(n=n)


__all__ = [
    "add_typos",
    "delete_random",
    "random_case_swap",
    "random_lower",
    "random_spaces",
    "random_string",
    "random_upper",
    "swap_random",
]
