from config import MODULE_SLOTS, MODULE_STATS, BEACON_BUILTIN_AMOUNTS

def module_beacon_selection_menu(main_menu_callback, machine):

    def module_selection(machine):
        print ("\n== Module Selection ==")
        print ("Can you enter what module type you want in the machine.")

        if machine not in MODULE_SLOTS:
            print(f"{machine} has zero slots or isn't in config")
            return None

        machine_slots = MODULE_SLOTS[machine]
        print(f"{machine} has {machine_slots} slots")

        if machine == "beacon":
            for name, stats in MODULE_STATS.items():
                if stats["speed"] > 0:
                    print(f"  {name}: {stats['speed']} speed")
        else:
            for name, stats in MODULE_STATS.items():
                print(f"  {name}: {stats['speed']} speed, {stats['prod']} productivity")
        print("you can chose the same modules twice or different ones. example (production3 speed3)")

        try:
            choice = input("example inputs: 'speed2' 'production3'\n> ").strip().lower()
        except ValueError:
            print ("Invalid input.")
            return module_selection(machine)
        if choice == "menu":
            return None

        module_type_machine = choice.split()

        if len(module_type_machine) > machine_slots:
            print (f"Invalid input. Please only enter {machine_slots} modules.")
            return module_selection(machine)
        for m in module_type_machine:
            if m not in MODULE_STATS.keys():
                print ("Invalid input. Please enter a valid module type.")

        speed_stats = sum(MODULE_STATS[m]["speed"] for m in module_type_machine)
        prod_stats = sum(MODULE_STATS[m]["prod"] for m in module_type_machine)
        if machine == "beacon":
            return speed_stats, module_type_machine
        return speed_stats, prod_stats, module_type_machine

    def beacon_selection():
        print ("\n== Beacon Selection ==")
        print ("you have the option to use a pre-made option or custom for your beacon amount.")
        print ("you will have the option to return to pick a different option. Just type back")

        try:
            choice = input("pre-made or custom\n> ").strip().lower()
        except ValueError:
            print ("Invalid input.")
            return beacon_selection()

        if choice == "menu":
            return None
        elif choice == "pre-made":
            for tire, amount in BEACON_BUILTIN_AMOUNTS.items():
                print(f"{tire}: has {amount} beacons")
        elif choice == "custom":
            print ("the max beacons is 12")
        else:
            print ("Invalid input.")
            return beacon_selection()

        choice2 = input("enter your amount\n> ").strip().lower()
        if choice2 == "menu":
            return None
        if choice2 == "back":
            return beacon_selection()

        try:
            choice2 = int(choice2)
        except ValueError:
            choice2 = BEACON_BUILTIN_AMOUNTS[choice2]
            choice2 = int(choice2)

        if choice2 > 12:
            print ("Invalid input. You can't have more then 12 beacons")
            return beacon_selection()
        elif choice2 < 0:
            print ("Invalid input. You can't have less then 0")
            return beacon_selection()

        print (f"you have selected {choice2} beacons. sending you to select modules for the beacons.")
        beacon_amount = choice2
        beacon_speed_stats, module_type_beacon = module_selection("beacon")

        return beacon_amount, beacon_speed_stats, module_type_beacon

    def module_beacon_selection():
        print ("\n== Modules and Beacon selection ==")
        print ("Do you want to proceed with or without modules and beacons.")
        try:
            module_beacon_choice = input("\n with/without.\n> ")
        except ValueError:
            print ("Invalid input. Please enter 'with' or 'without'.")
            return main_menu_callback()
        return module_beacon_choice

    module_beacon_choice = module_beacon_selection()
    if module_beacon_choice == "menu":
        return main_menu_callback()
    elif module_beacon_choice == "with":
        print("proceeding with modules and beacons")
    elif module_beacon_choice == "without":
        print("proceeding without modules and beacons")
        return "without"
    else:
        print("Invalid choice. Please try again.")
        return module_beacon_selection()

    module_selection_stats = module_selection(machine)
    if module_selection_stats is None:
        main_menu_callback()
    speed_stats, prod_stats, module_type_machine = module_selection_stats

    beacon_selection_stats = beacon_selection()
    if beacon_selection_stats is None:
        main_menu_callback()
    beacon_amount, per_beacon_speed_stats, module_type_beacon = beacon_selection_stats

    return speed_stats, prod_stats, beacon_amount, per_beacon_speed_stats, module_type_machine, module_type_beacon, "with"