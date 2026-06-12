from comnet.shared.dicts.country_dict import COUNTRY_TO_COLOR
from comnet.visualizer.full_analysis import do_full_analysis
from comnet.visualizer.utils import get_allies_edges_w, get_com_to_country, get_enemies_edges_w
from comnet.config import pipeline_type


def main():
    allies = get_allies_edges_w()
    enemies = get_enemies_edges_w()

    do_full_analysis(allies, enemies, get_com_to_country(f"data/{pipeline_type}/normalized/commanders.csv"), COUNTRY_TO_COLOR)

if __name__ == "__main__":
    main()