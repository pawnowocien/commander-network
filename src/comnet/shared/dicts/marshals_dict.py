from comnet.shared.dicts.ww1.marshals_dict import HIGH_RANKED as HIGH_RANKED_WW1
from comnet.shared.dicts.ww2.marshals import HIGH_RANKED as HIGH_RANKED_WW2

from comnet.config import pipeline_type

dict_setup = {
    "ww1": {
        "high_ranked": HIGH_RANKED_WW1
    },
    "ww2": {
        "high_ranked": HIGH_RANKED_WW2
    }
}

HIGH_RANKED = dict_setup[pipeline_type]["high_ranked"]
HIGH_RANKED_SET = set(HIGH_RANKED)