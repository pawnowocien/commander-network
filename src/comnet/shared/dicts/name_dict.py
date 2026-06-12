from comnet.shared.dicts.ww1.name_dict import (
    CLEAN_NAME_DICT as CLEAN_NAME_DICT_WW1, 
    COMPLEX_NAME_DICT as COMPLEX_NAME_DICT_WW1
)

from comnet.shared.dicts.ww2.name_dict import (
    COMPLEX_NAME_DICT as COMPLEX_NAME_DICT_WW2,
)

# For normalizing letters in names
LETTER_DICT = {
    "ß": "ss"
}

# For common (first) names that are often spelt differently, but refer to the same person.
# Sorry if the names are not in the correct language!
SIMPLE_NAME_DICT = {
    "Aleksei": "Aleksei",
    "Alexei": "Aleksei",
    "Alexey": "Aleksei",
}

COMPLEX_NAME_DICT = {**COMPLEX_NAME_DICT_WW1, **COMPLEX_NAME_DICT_WW2}
CLEAN_NAME_DICT = CLEAN_NAME_DICT_WW1