"""TASK 06 · region table shared by every vegetation script (library builder, sheet render / compose, QC, contact sheet).

prefix → library name; map region codes (approved map rev 01 + Decision Sheet 01 mapping). Milestone 1 = AV EF MK, milestone 2 = rest.
Sky Realms (PROPOSED region, map position PENDING) has NO library of its own: it re-uses the main-world spring flora (Decision 01 §2).
"""
import t6_species as SP, t6_plants as PL, t6_species_m2 as SP2, t6_plants_m2 as PL2

NAMES = {'AV': 'ASHRAM_VALLEY', 'EF': 'ENCHANTED_FOREST', 'MK': 'MOUNTAIN_KINGDOM',
         'PL': 'GREEN_PLAINS', 'LK': 'CRYSTAL_LAKES', 'DS': 'GOLDEN_DESERT', 'FB': 'FORBIDDEN_LANDS',
         'CT': 'ANCIENT_CITY_SITES', 'CV': 'HIDDEN_UNDERGROUND'}
CODES = {'AV': 'R-01', 'EF': 'R-02', 'MK': 'R-03', 'PL': 'R-06', 'LK': 'R-08', 'DS': 'R-04', 'FB': 'R-05',
         'CT': 'C-01 / C-02 / C-03', 'CV': 'CV-01…05'}
TITLES = {'AV': 'ASHRAM VALLEY', 'EF': 'ENCHANTED FOREST', 'MK': 'MOUNTAIN KINGDOM (Great Northern Range)',
          'PL': 'GREEN PLAINS (Southern Grasslands)', 'LK': 'CRYSTAL LAKES (Lake District)', 'DS': 'GOLDEN DESERT (Western Desert)',
          'FB': 'FORBIDDEN LANDS (crater)', 'CT': 'ANCIENT CITY SURROUNDINGS (3 separate sites)', 'CV': 'HIDDEN UNDERGROUND (caves)'}
M1 = ('AV', 'EF', 'MK'); M2 = ('PL', 'LK', 'DS', 'FB', 'CT', 'CV')

TREES = SP.TREES + SP2.TREES
SHRUBS = SP.SHRUBS + SP2.SHRUBS
PLANTS = PL.PLANTS + PL2.PLANTS
M2_NAMES = {d['name'] for d in SP2.TREES + SP2.SHRUBS + PL2.PLANTS}


def region_of(name):
    return name.split('_')[0]


def build_plant(D, seed=0, collection=None):
    """dispatch: milestone-2 plants (new builders / material kinds) through t6_plants_m2, the rest unchanged."""
    return (PL2 if D['name'] in M2_NAMES else PL).build_plant(D, seed, collection)


def build_woody(D, seed=0, collection=None):
    """trees + shrubs: palms through t6kit_m2.build_palm, everything else the standard generator."""
    import t6kit as K, t6_matlib as ML
    if D.get('builder') == 'palm':
        import t6kit_m2 as K2
        return K2.build_palm(D, seed, collection, K2.palm_mats(D))
    return K.build_tree(D, seed, collection, ML.species_mats(D))
