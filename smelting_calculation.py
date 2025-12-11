from config import (
    STONE_FURNACE_BASE_RATES,
    STEEL_ELECTRIC_FURNACE_BASE_RATES,
    STONE_INPUT,
    COAL_FURNACE_BASE_RATES,
)
from math import ceil
from collections import Counter


def calculation(IMPORTANT_VALUES_SMELTING):

    def ore_rate(IMPORTANT_VALUES_SMELTING):
        try:
            furnace = IMPORTANT_VALUES_SMELTING["furnace"]
            ore = IMPORTANT_VALUES_SMELTING["ore"]
            module_beacon_choice = IMPORTANT_VALUES_SMELTING["module_beacon_choice"]
            speed_stats = IMPORTANT_VALUES_SMELTING["speed_stats"]
            prod_stats = IMPORTANT_VALUES_SMELTING["prod_stats"]
            beacon_amount = IMPORTANT_VALUES_SMELTING["beacon_amount"]
            beacon_speed_stats = IMPORTANT_VALUES_SMELTING["beacon_speed_stats"]
        except KeyError as e:
            return f"missing key in IMPORTANT_VALUES_SMELTING: {e}"

        try:
            if furnace == "stone":
                base_rate = STONE_FURNACE_BASE_RATES[ore]
            elif furnace in ("steel", "electric"):
                base_rate = STEEL_ELECTRIC_FURNACE_BASE_RATES[ore]
            else:
                return f"invalid furnace type: {furnace}"
        except KeyError as e:
            return f"missing ore rate for {ore} in furnace type {furnace}: {e}"

        try:
            if module_beacon_choice == "without":
                return base_rate

            total_speed_stats = speed_stats + (beacon_amount * beacon_speed_stats)
            total_prod_stats = prod_stats
            return base_rate * (1 + total_speed_stats) * (1 + total_prod_stats)
        except Exception as e:
            return f"error during calculation: {e}"


    def furnace_needed(IMPORTANT_VALUES_SMELTING):
        try:
            ips = IMPORTANT_VALUES_SMELTING["ips_output"]
            production_rate = IMPORTANT_VALUES_SMELTING["production_rate"]
        except KeyError as e:
            return f"missing key in IMPORTANT_VALUES_SMELTING: {e}"

        try:
            furnace_needed = ceil(ips / production_rate)
        except Exception as e:
            return f"error during furnace calculation: {e}"

        return furnace_needed

    def belt_needed(IMPORTANT_VALUES_SMELTING):
        try:
            ips = IMPORTANT_VALUES_SMELTING["ips_output"]
            belt_speed = IMPORTANT_VALUES_SMELTING["belt_speed"]
            ore = IMPORTANT_VALUES_SMELTING["ore"]
        except KeyError as e:
            return f"missing key in IMPORTANT_VALUES_SMELTING: {e}"

        try:
            if ore == "stone brick":
                stone_needed_per_second = STONE_INPUT[IMPORTANT_VALUES_SMELTING["furnace"]] * IMPORTANT_VALUES_SMELTING["furnace_needed"]
                return ceil(stone_needed_per_second / belt_speed)
            elif ore in ("steel plate", "iron plate", "copper plate"):
                return ceil(ips / belt_speed)
            else:
                return f"invalid ore: {ore}"
        except KeyError as e:
            return f"missing key in IMPORTANT_VALUES_SMELTING: {e}"
        except Exception as e:
            return f"error during belt calculation: {e}"

    def coal_needed(IMPORTANT_VALUES_SMELTING):
        try:
            furnace_needed = IMPORTANT_VALUES_SMELTING["furnace_needed"]
            furnace = IMPORTANT_VALUES_SMELTING["furnace"]
        except KeyError as e:
            return f"missing key in IMPORTANT_VALUES_SMELTING: {e}"

        try:
            if furnace in ("stone", "steel"):
                return ceil(COAL_FURNACE_BASE_RATES * furnace_needed)
            elif furnace == "electric":
                return 0
            else:
                return f"invalid furnace type: {furnace}"
        except Exception as e:
            return f"error during coal calculation: {e}"

    def beacon_total(IMPORTANT_VALUES_SMELTING):
        try:
            furnace_needed = IMPORTANT_VALUES_SMELTING["furnace_needed"]
            beacon_amount= IMPORTANT_VALUES_SMELTING["beacon_amount"]
            module_beacon_choice = IMPORTANT_VALUES_SMELTING["module_beacon_choice"]
        except KeyError as e:
            return f"missing key in IMPORTANT_VALUES_SMELTING: {e}"

        try:
            if module_beacon_choice == "without":
                return 0

            return furnace_needed * beacon_amount
        except Exception as e:
            return f"error during beacon calculation: {e}"


    def module_total(IMPORTANT_VALUES_SMELTING):
        try:
            furnace_needed = IMPORTANT_VALUES_SMELTING["furnace_needed"]
            beacon_amount= IMPORTANT_VALUES_SMELTING["beacon_amount"]
            module_beacon_choice = IMPORTANT_VALUES_SMELTING["module_beacon_choice"]
            module_type_machine = IMPORTANT_VALUES_SMELTING["module_type_machine"]
            module_type_beacon = IMPORTANT_VALUES_SMELTING["module_type_beacon"]
        except KeyError as e:
            return f"missing key in IMPORTANT_VALUES_SMELTING: {e}"

        try:
            total_furnace_modules = {}
            total_beacon_modules = {}
            total_modules = 0

            if module_beacon_choice == "without":
                return 0, 0, 0

            count_furnace_modules_output = Counter(module_type_machine)
            count_beacon_modules_output = Counter(module_type_beacon)

            for module_type, count in count_furnace_modules_output.items():
                total_furnace_modules[module_type] = count * furnace_needed

            for module_type, count in count_beacon_modules_output.items():
                total_beacon_modules[module_type] = count * beacon_amount

            for module_type in set(total_furnace_modules) | set(total_beacon_modules):
                total_modules += total_furnace_modules.get(module_type, 0) + total_beacon_modules.get(module_type, 0)

            return total_modules, total_furnace_modules, total_beacon_modules
        except Exception as e:
            return f"error during module calculation: {e}"

    def calculation_run(IMPORTANT_VALUES_SMELTING):
        production_rate_output = ore_rate(IMPORTANT_VALUES_SMELTING)
        if isinstance(production_rate_output, str):
            print ("error in ore_rate: ", production_rate_output)
            exit()
        IMPORTANT_VALUES_SMELTING["production_rate"] = production_rate_output

        furnace_needed_output = furnace_needed(IMPORTANT_VALUES_SMELTING)
        if isinstance(furnace_needed_output, str):
            print("error: in furnace_needed ", furnace_needed_output)
            exit()
        IMPORTANT_VALUES_SMELTING["furnace_needed"] = furnace_needed_output

        belt_needed_output = belt_needed(IMPORTANT_VALUES_SMELTING)
        if isinstance(belt_needed_output, str):
            print("error: in belt_needed", belt_needed_output)
            exit()
        IMPORTANT_VALUES_SMELTING["belt_needed"] = belt_needed_output

        coal_needed_output = coal_needed(IMPORTANT_VALUES_SMELTING)
        if isinstance(coal_needed_output, str):
            print("error: in coal_needed", coal_needed_output)
            exit()
        IMPORTANT_VALUES_SMELTING["coal_needed"] = coal_needed_output

        beacon_total_output = beacon_total(IMPORTANT_VALUES_SMELTING)
        if isinstance(beacon_total_output, str):
            print("error: in beacon_total", beacon_total_output)
            exit()
        IMPORTANT_VALUES_SMELTING["beacon_total"] = beacon_total_output

        module_total_output = module_total(IMPORTANT_VALUES_SMELTING)
        if isinstance(module_total_output, str):
            print("error: in module_total", module_total_output)
            exit()
        total_modules, total_furnace_modules, total_beacon_modules = module_total_output
        IMPORTANT_VALUES_SMELTING["total_modules"] = total_modules
        IMPORTANT_VALUES_SMELTING["total_furnace_modules"] = total_furnace_modules
        IMPORTANT_VALUES_SMELTING["total_beacon_modules"] = total_beacon_modules

        return IMPORTANT_VALUES_SMELTING

    def iron_if_steel_config(values_transfer):
        iron_config = {
            "ore": "iron plate",
            "ips_output": values_transfer["ips_output"] * 5,
            "belt_name": values_transfer["belt_name"],
            "belt_speed": values_transfer["belt_speed"],
            "furnace": values_transfer["furnace"],
            "speed_stats": values_transfer["speed_stats"],
            "prod_stats": values_transfer["prod_stats"],
            "beacon_amount": values_transfer["beacon_amount"],
            "beacon_speed_stats": values_transfer["beacon_speed_stats"],
            "module_type_machine": values_transfer["module_type_machine"],
            "module_type_beacon": values_transfer["module_type_beacon"],
            "module_beacon_choice": values_transfer["module_beacon_choice"],
        }
        iron_sub_output = calculation_run(iron_config)
        return iron_sub_output

    def iron_if_steel(IMPORTANT_VALUES_SMELTING):
        try:
            if IMPORTANT_VALUES_SMELTING["ore"] == "steel plate":
                iron_sub_recipe = iron_if_steel_config(IMPORTANT_VALUES_SMELTING)
                IMPORTANT_VALUES_SMELTING_output = calculation_run(IMPORTANT_VALUES_SMELTING)
                smelting_values = IMPORTANT_VALUES_SMELTING_output | {"iron_sub_recipe": iron_sub_recipe}
            elif IMPORTANT_VALUES_SMELTING["ore"] in ("iron plate", "copper plate", "stone brick"):
                IMPORTANT_VALUES_SMELTING_output = calculation_run(IMPORTANT_VALUES_SMELTING)
                smelting_values = IMPORTANT_VALUES_SMELTING_output
            else:
                print("Invalid ore type.")
                exit()

            return smelting_values
        except KeyError as e:
            print (f"error: missing key in IMPORTANT_VALUES_SMELTING: {e}")
            exit()

    return iron_if_steel(IMPORTANT_VALUES_SMELTING)