import mwparserfromhell as mwp
from models.models import Country

# Works for simple cases
def parse_combatant(combatant_code: mwp.wikicode.Wikicode) -> list[Country]:
    countries = []
    for node in combatant_code.nodes:
        # With flagicons
        if isinstance(node, mwp.nodes.Template):
            if node.name.strip().lower() == "flagcountry":
                country_name = node.get(1).value.strip_code().strip()
                countries.append(Country(name=country_name))
        # Without flagicons
        elif isinstance(node, mwp.nodes.Wikilink):
            country_name = node.title.strip_code().strip()
            countries.append(Country(name=country_name))
    return countries