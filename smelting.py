# this is the old code befoe i split it up into multiple files. i left this here for reference so i could make the new code better and build of this

from config import BELT_SPEEDS, STONE_FURNACE_BASE_RATES, STEEL_ELECTRIC_FURNACE_BASE_RATES, COAL_FURNACE_BASE_RATES, STONE_INPUT
from modules import module_selection_menu
from math import ceil

def smelting_menu_finally(main_menu_callback):
    print ("\n== Smelting Completed ==")
    choice = input("Do you want to return to the main menu? yes/no\n> ").strip().lower()
    if choice == "yes" or choice == "y" or choice == "menu":
        return main_menu_callback()
    elif choice == "no" or choice == "n":
        return smelting_menu(main_menu_callback)
    else:
        print ("Invalid choice. Please try again.")
        return smelting_menu_finally(main_menu_callback)

def print_smelting_results(main_menu_callback, IMPORTANT_VALUES):

    print ("\n== Furnace Calculations ===")
    if IMPORTANT_VALUES["module_choice"] == "without":
        print (f"you will need: ")
        print (f"{IMPORTANT_VALUES["furnace_needed_base"]} {IMPORTANT_VALUES["ore"]} furnaces of {IMPORTANT_VALUES["furnace"]} type")
        print (f"belt type: {IMPORTANT_VALUES["belt_name"]} going {IMPORTANT_VALUES["belt_speed"]}/s")
        print (f"{IMPORTANT_VALUES["inputted_belts"]} input belts for {IMPORTANT_VALUES["ore"]}")
        print(f"{IMPORTANT_VALUES["inputted_belts"]} input belts of {IMPORTANT_VALUES["ore"]}")
        print(f"{IMPORTANT_VALUES["outputted_belts"]} output belts of {IMPORTANT_VALUES["ore"]}")

        if IMPORTANT_VALUES["ore"] == "steel":
            print(f"{IMPORTANT_VALUES["furnace_needed_iron"]} iron furnaces")
            print(f"{IMPORTANT_VALUES["iron_input_belts"]} iron input belts")

        if IMPORTANT_VALUES["furnace"] in ("stone", "steel"):
            print(f"input of {IMPORTANT_VALUES["coal_needed"]}/s coal")
    elif IMPORTANT_VALUES["module_choice"] == "with":
        print (f"you will need: ")
    return smelting_menu_finally(main_menu_callback)

def furnace_calculations(main_menu_callback, IMPORTANT_VALUES):

    def ore_rate (IMPORTANT_VALUES):
        furnace = IMPORTANT_VALUES["furnace"]
        ore = IMPORTANT_VALUES["ore"]
        ORE_RATE_iron = 0

        if furnace == "stone":
            ORE_RATE = STONE_FURNACE_BASE_RATES[ore]
            if IMPORTANT_VALUES["ore"] == "steel":
                ORE_RATE_iron = STONE_FURNACE_BASE_RATES["iron"]

        elif furnace in ("steel", "electric"):
            ORE_RATE = STEEL_ELECTRIC_FURNACE_BASE_RATES[ore]
            if IMPORTANT_VALUES["ore"] == "steel":
                ORE_RATE_iron = STONE_FURNACE_BASE_RATES["iron"]

        else:
            return None

        if ORE_RATE is None:
            return None
        return ORE_RATE, ORE_RATE_iron

    def belt(IMPORTANT_VALUES):
        items_pers = IMPORTANT_VALUES["ips"]
        belt_speed = IMPORTANT_VALUES["belt_speed"]
        furnace_needed = IMPORTANT_VALUES["furnace_needed"]

        if IMPORTANT_VALUES["ore"] in ("iron", "copper"):
            return ceil(items_pers / belt_speed)

        elif IMPORTANT_VALUES["ore"] == "steel":
            steel_output_ps = ceil(items_pers / belt_speed)
            iron_needed_pers = steel_output_ps * 5
            iron_input_belts = iron_needed_pers / belt_speed
            return steel_output_ps, iron_input_belts

        elif IMPORTANT_VALUES["ore"] == "stone brick":
            return ceil((STONE_INPUT[IMPORTANT_VALUES["furnace"]] * furnace_needed) // belt_speed)

        else:
            return None

    def furnace_needed(main_menu_callback, IMPORTANT_VALUES):
        ips = IMPORTANT_VALUES["ips"]
        ORE_RATE_output = ore_rate(IMPORTANT_VALUES)
        if ORE_RATE_output is None:
            print("config may be missing data. returning to main menu.")
            return main_menu_callback()
        ORE_RATE, ORE_RATE_iron = ORE_RATE_output

        module_choice = module_selection_menu(main_menu_callback, IMPORTANT_VALUES)
        if module_choice == None:
            furnace_needed = ceil(ips / ORE_RATE)
            furnace_needed_iron = ceil(ips / ORE_RATE_iron)
            IMPORTANT_VALUES["module_beacon_choice_base"] = "without"
            return furnace_needed, furnace_needed_iron

        speed_stats, prod_stats, beacon_amount, beacon_speed_stats = module_choice.split()

    def coal_usage(IMPORTANT_VALUES):
        furnace = IMPORTANT_VALUES["furnace"]
        furnace_needed = IMPORTANT_VALUES["furnace_needed"]
        ore = IMPORTANT_VALUES["ore"]

        if furnace in ("stone", "steel"):
            if ore == "steel":
                iron_furnaces = IMPORTANT_VALUES["iron_furnaces"]

                coal_needed = ceil(COAL_FURNACE_BASE_RATES * (furnace_needed + iron_furnaces))
            elif ore in ("copper", "iron", "stone brick"):
                coal_needed = ceil(COAL_FURNACE_BASE_RATES * furnace_needed)
            else:
                return None, None
        elif furnace == "electric":
            coal_needed = 0
        else:
            return None
        return coal_needed

    ips = IMPORTANT_VALUES["ips"]
    belt_speed = IMPORTANT_VALUES["belt_speed"]

    furnace_needed_output = furnace_needed(main_menu_callback, IMPORTANT_VALUES)
    if furnace_needed_output is None:
        print ("config may be missing data. returning to main menu.")
        return main_menu_callback()
    furnace_needed, iron_furnaces = furnace_needed_output.split()
    IMPORTANT_VALUES["furnace_needed_base"] = furnace_needed
    IMPORTANT_VALUES["furnace_needed_iron"] = iron_furnaces

    belt_output = belt(IMPORTANT_VALUES)
    if belt_output is None:
        print ("config may be missing data. returning to main menu.")
        return main_menu_callback()
    inputted_belts, inputted_belts_iron = belt_output.split()
    IMPORTANT_VALUES["inputted_belts_base"] = inputted_belts
    IMPORTANT_VALUES["inputted_belts_iron"] = inputted_belts_iron

    outputted_belts = ceil(ips // belt_speed)
    IMPORTANT_VALUES["outputted_belts"] = outputted_belts

    coal_needed = coal_usage(IMPORTANT_VALUES)
    if coal_needed is None:
        print ("error as no valid furnace found. returning to main menu.")
        return main_menu_callback()
    elif coal_needed == (None, None):
        print ("error as no valid ore found. returning to main menu.")
        return main_menu_callback()
    IMPORTANT_VALUES["coal_needed"] = coal_needed

    return print_smelting_results(main_menu_callback, IMPORTANT_VALUES)

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

    belt_result = belt_choice()
    if belt_result == (None, None):
        return main_menu_callback()
    items_per_second, belt_name = belt_result
    belt_speed = BELT_SPEEDS[belt_name]

    furnace = furnace_choice()
    if furnace is None:
        return main_menu_callback()

    IMPORTANT_VALUES = {
        "ips": items_per_second,
        "belt_name": belt_name,
        "belt_speed": belt_speed,
        "furnace": furnace,
        "ore": ore,
    }

    return furnace_calculations(main_menu_callback, IMPORTANT_VALUES)


def smelting_menu(main_menu_callback):

    print ("\n== Smelting Menu ==")
    print ("what ore are you smelling?")
    print("1. Iron \n2. Copper \n3. Steel \n4. Stone Brick \n5. Main Menu")

    try:
        choice = input("> ").strip().lower()
    except ValueError:
        print("Invalid input. Please enter a valid choice.")
        return smelting_menu(main_menu_callback)
    if choice == "5" or choice == "menu":
        return main_menu_callback()
    ore_selection_map = {
        "1": "iron",
        "2": "copper",
        "3": "steel",
        "4": "stone brick",
    }
    if choice not in ore_selection_map:
        print("Invalid choice. Please try again.")
        return smelting_menu(main_menu_callback)
    ore_selected = ore_selection_map[choice]
    return other_conditions(main_menu_callback, ore_selected)