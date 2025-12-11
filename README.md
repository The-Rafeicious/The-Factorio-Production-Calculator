# The-Factorio-Production-Calculator

## What it does
the program will run on command line and is entered in the ``main.py`` file. the code will then
run and ask the user for inputs and calculate variables from the inputs and pre loaded config
information. it is ment to calculate a bunch of variables but mainly calculates:
- amount of furnace's needed
- number of belts needed
- modules required if requested
- beacons required if requested

## The program files
``main.py`` is the main menu for the program. it has two options with smelting and exit.
it is designed to accommodate more functions but currently doesn't

``config.py`` this is the main variable file. it contains base variables that can't be entered by
the user. they are stored in dictionaries that can be imported into programs they are needed.

``smelting_options.py`` is the main input file in the code. it will ask the user for inputs such
as belts, amount of belts, ore, furnace type. it has a segment of code that will run and return
variables form ``modules.py``. with this information a large dictionary is created and transferred to
the main calculation file ``smelting_calculation.py``.

``smelting_calculations.py`` is the calculator in the program. it will take all the values and
output them to be printed. nothing is printed in the program except for error notifications when a
error is detected. once completed it will pass on the values to ``smelting_print.py``.

``smelting_print.py`` this is a simple print it uses json to dump/print all the values from the program
it doesn't hold back any data and prints everything processed.

``modules.py`` this is a standalone program that can be run from future processes other than smelting.
it has an input and will ask the user about the number of beacons and module types. it will
return all the values to the program that called it.

``test.py`` this is a test program that I asked AI to create for me. I don't fully understand how
it works, but it did help me fix some errors in the code.

``smelting.py`` this is an old program. it originally had all the ``smelting_`` programs contained inside
but I split it up to run better and be easier to diagnose problems. i have left it to examine and improve
of the code there.
