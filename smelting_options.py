from config import BELT_SPEEDS
from math import ceil
from modules import module_beacon_selection_menu
from smelting_calculation import calculation
from smelting_print import smelting_print_menu

def other_conditions(main_menu_callback, ore):
    def belt_choice():
        print ("\n== Belt Choice ==")
        print ("Can you enter what belt type you want to output.")
        for name, speed in BELT_SPEEDS.items():
            print (f"{name}: {speed} Items per second")
        belt = input("> ").strip().lower()
        if belt == "menu":
            return None, None
        if belt not in BELT_SPEEDS:
            print ("Invalid choice. Please try again.")
            return belt_choice()

        print ("\n== Belt Amount ==")
        try:
            amount_str = input("How Many belts do you want to calculate?\n> ").strip().lower()
            if amount_str == "menu":
                return None, None
            amount = int(amount_str)
        except ValueError:
            print ("Invalid input. Please enter a number.")
            return belt_choice()

        items_per_second = ceil(amount * BELT_SPEEDS[belt])
        return items_per_second, belt

    def furnace_choice():
        print ("\n== Furnace Choice ==")
        print ("Can you enter what furnace type you want to output.\nStone, Steel or Electric.")
        try:
            furnace = input("> ").strip().lower()
        except ValueError:
            print ("Invalid input. Please enter a valid furnace type.")
            return furnace_choice()
        if furnace == "menu":
            return None

        return furnace

    def module_selection_options():
        output = module_beacon_selection_menu(
            main_menu_callback,
            furnace,
        )

        MODULE_DEFAULTS = {
            "speed_stats": 0,
            "prod_stats": 0,
            "beacon_amount": 0,
            "beacon_speed_stats": 0,
            "module_type_machine": [],
            "module_type_beacon": [],
            "module_beacon_choice": "without",
        }

        if output == "without":
            module_values = MODULE_DEFAULTS.copy()
        else:
            speed_stats, prod_stats, beacon_amount, beacon_speed_stats, module_type_machine, module_type_beacon, module_beacon_choice = output
            module_values = {
                "speed_stats": speed_stats,
                "prod_stats": prod_stats,
                "beacon_amount": beacon_amount,
                "beacon_speed_stats": beacon_speed_stats,
                "module_type_machine": module_type_machine,
                "module_type_beacon": module_type_beacon,
                "module_beacon_choice": module_beacon_choice,
            }
        return module_values

    belt_result = belt_choice()
    if belt_result == (None, None):
        return main_menu_callback()
    items_per_second, belt_name = belt_result
    belt_speed = BELT_SPEEDS[belt_name]

    furnace = furnace_choice()
    if furnace is None:
        return main_menu_callback()

    module_values = module_selection_options()


    IMPORTANT_VALUES_SMELTING = {
        "ore": ore,
        "ips_output": items_per_second,
        "belt_name": belt_name,
        "belt_speed": belt_speed,
        "furnace": furnace,
    } | module_values

    calalculation_values = calculation(IMPORTANT_VALUES_SMELTING)
    return smelting_print_menu(main_menu_callback, calalculation_values)


def smelting_menu(main_menu_callback):

    print ("\n== Smelting Menu ==")
    print ("what ore are you smelling?")
    print("1. Iron ore --> Iron plate \n2. Copper ore --> Copper plate")
    print ("3. Iron plate --> Steel plate \n4. Stone --> Stone brick \n5. Main Menu")

    try:
        choice = input("> ").strip().lower()
    except ValueError:
        print("Invalid input. Please enter a valid choice.")
        return smelting_menu(main_menu_callback)
    if choice == "5" or choice == "menu":
        return main_menu_callback()
    ore_selection_map = {
        "1": "iron plate",
        "2": "copper plate",
        "3": "steel plate",
        "4": "stone brick",
    }
    if choice not in ore_selection_map:
        print("Invalid choice. Please try again.")
        return smelting_menu(main_menu_callback)
    ore_selected = ore_selection_map[choice]
    return other_conditions(main_menu_callback, ore_selected)