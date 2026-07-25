from math import ceil

from config import BELT_SPEEDS, MODULE_DEFAULTS
from smelting_calculation import calculation


def smelting_form_base (FORM_DATA):

    def sf_processing (ba, b):
        ips = ceil(ba * BELT_SPEEDS[b])
        bs = BELT_SPEEDS[b]
        return ips, bs

    ore_type = FORM_DATA.get("ore_type")
    belt_type = FORM_DATA.get("belt_type")
    belt_no = int(FORM_DATA.get("belt_no"))
    furnace_type = FORM_DATA.get("furnace_type")

    sf_belt_results = sf_processing(belt_no, belt_type)
    ips, belt_speed = sf_belt_results

    FORM_DATA_ORGNISED = {
        "ore": ore_type,
        "ips_output": ips,

        "belt_name": belt_type,
        "belt_speed": belt_speed,

        "furnace": furnace_type,
    } | MODULE_DEFAULTS

    CALCULATION_RESULTS = calculation(FORM_DATA_ORGNISED)
    return CALCULATION_RESULTS