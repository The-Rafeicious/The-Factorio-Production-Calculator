import json

def smelting_print_menu(main_menu_callback, calalculation_values):
    print("\n== Smelting Calculation Results ==")
    print("Smelting calculation completed successfully.")
    print("Displaying smelting calculation results...")
    print(json.dumps(calalculation_values, indent=4))
    return main_menu_callback()