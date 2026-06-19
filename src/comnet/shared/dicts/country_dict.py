from comnet.shared.dicts.ww1.country_dict import (
    NORMALIZE_COUNTRY_NAME as NORMALIZE_COUNTRY_NAME_WW1, 
    NAME_TO_COUNTRY as NAME_TO_COUNTRY_WW1,
    COUNTRY_TO_COLOR as COUNTRY_TO_COLOR_WW1,
)

from comnet.shared.dicts.ww2.country_dict import (
    NORMALIZE_COUNTRY_NAME as NORMALIZE_COUNTRY_NAME_WW2,
    COUNTRY_TO_COLOR as COUNTRY_TO_COLOR_WW2,
    NAME_TO_COUNTRY as NAME_TO_COUNTRY_WW2
)


NAME_TO_COUNTRY = {**NAME_TO_COUNTRY_WW1, **NAME_TO_COUNTRY_WW2}




from comnet.config import pipeline_type

dict_setup = {
    "ww1": {
        "norm_country": NORMALIZE_COUNTRY_NAME_WW1,
        "country_to_color": COUNTRY_TO_COLOR_WW1,
    },
    "ww2": {
        "norm_country": NORMALIZE_COUNTRY_NAME_WW2,
        "country_to_color": COUNTRY_TO_COLOR_WW2,
    }
}

NORMALIZE_COUNTRY_NAME = dict_setup[pipeline_type]["norm_country"]
COUNTRY_TO_COLOR = dict_setup[pipeline_type]["country_to_color"]