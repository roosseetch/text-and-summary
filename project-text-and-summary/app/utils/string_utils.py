import re


def strip_special_characters(s: str) -> str:
    """Return the sting with stripped special charaters

    >>> from app.utils.string_utils import strip_special_characters
    >>> strip_special_characters('')
    ''
    >>> strip_special_characters('&(*)(**^*')
    ''
    >>> strip_special_characters('&(*)(**^*tweywiew*^*&(ieuweer79789')
    'tweywiew*^*&(ieuweer79789'
    >>> strip_special_characters('&(*)(**^*tweywiew*^*&(ieuweer79789^&*')
    'tweywiew*^*&(ieuweer79789'
    >>> strip_special_characters('tweywiew*^*&(ieuweer79789^&*')
    'tweywiew*^*&(ieuweer79789'
    >>> strip_special_characters('@U#')
    'U'
    """
    beginning_of_str: int | None = None
    end_of_str: int | None = None
    pattern = r'[a-zA-Z0-9]'

    for left_index in range(len(s)):

        # break iteration if we already found beggining and end of string
        if beginning_of_str is not None and end_of_str is not None:
            break

        right_index = -1 - left_index

        # break iterations if we already checked all characters in the string
        if (beginning_of_str if beginning_of_str is not None else left_index) - right_index > len(s):
            break

        if beginning_of_str is None and re.match(pattern, s[left_index]):
            beginning_of_str = left_index

        if end_of_str is None and re.match(pattern, s[right_index]):
            end_of_str = right_index + 1 if right_index != -1 else len(s)

    return s[beginning_of_str or 0 : end_of_str or 0]
