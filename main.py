from  smelting_options import smelting_menu

def main_menu():

    print ("\n==The Factorio Production Calculator==")
    print ("You can type 'menu' at any point to return here")
    print ("------------------------------")
    print ("chose and option of what process you want carried out")
    print ("1. smelting calculator")
    print ("2. exit")

    menu_choice = int(input("> "))

    if menu_choice == 1:
        smelting_menu(main_menu)
    elif menu_choice == 2:
        exit()



if __name__ == '__main__':
    main_menu()