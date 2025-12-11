import unittest
from math import ceil
# Import the config values so the test adapts to your specific numbers
from config import STONE_FURNACE_BASE_RATES, STEEL_ELECTRIC_FURNACE_BASE_RATES
from smelting_calculation import calculation


class TestFactorioSmelting(unittest.TestCase):

    def get_base_config(self):
        """Helper to create a default configuration dictionary."""
        return {
            "ore": "iron plate",
            "ips_output": 15,  # 1 yellow belt
            "belt_name": "yellow",
            "belt_speed": 15,
            "furnace": "stone",
            "module_beacon_choice": "without",
            "speed_stats": 0,
            "prod_stats": 0,
            "beacon_amount": 0,
            "beacon_speed_stats": 0,
            "module_type_machine": [],
            "module_type_beacon": []
        }

    def test_basic_iron_stone_furnace(self):
        """Test 1: Basic Iron Plate in Stone Furnace"""
        print("\nRunning Test: Basic Iron Plate...")

        config = self.get_base_config()

        # Calculate EXPECTED value dynamically based on config
        base_rate = STONE_FURNACE_BASE_RATES["iron plate"]
        expected_furnaces = ceil(config["ips_output"] / base_rate)

        result = calculation(config)

        print(f"   Rate: {base_rate}, Output: {result['furnace_needed']} (Expected: {expected_furnaces})")
        self.assertEqual(result["furnace_needed"], expected_furnaces)

    def test_steel_production(self):
        """Test 2: Steel Plate (Requires recursive iron calculation)"""
        print("\nRunning Test: Steel Plate...")

        config = self.get_base_config()
        config["ore"] = "steel plate"
        config["furnace"] = "stone"
        config["ips_output"] = 1.0

        result = calculation(config)

        # Dynamic check for Steel
        steel_base_rate = STONE_FURNACE_BASE_RATES["steel plate"]
        expected_steel_furnaces = ceil(1.0 / steel_base_rate)

        self.assertEqual(result["furnace_needed"], expected_steel_furnaces)

        # Dynamic check for Iron Sub-recipe
        # Steel requires 5 iron per 1 steel (standard recipe)
        iron_needed = 1.0 * 5
        iron_base_rate = STONE_FURNACE_BASE_RATES["iron plate"]
        expected_iron_furnaces = ceil(iron_needed / iron_base_rate)

        self.assertEqual(result["iron_sub_recipe"]["furnace_needed"], expected_iron_furnaces)

    def test_electric_furnace_with_modules(self):
        """Test 3: Electric Furnace with Speed Modules"""
        print("\nRunning Test: Electric Furnace with Speed Modules...")

        config = self.get_base_config()
        config["furnace"] = "electric"
        config["module_beacon_choice"] = "with"
        config["speed_stats"] = 1.0  # +100% speed

        result = calculation(config)

        # Dynamic Calculation
        base_rate = STEEL_ELECTRIC_FURNACE_BASE_RATES["iron plate"]
        # Formula: Base * (1 + speed) * (1 + prod)
        calc_rate = base_rate * (1 + config["speed_stats"])
        expected_furnaces = ceil(config["ips_output"] / calc_rate)

        print(f"   Base Rate: {base_rate}")
        print(f"   Calc Rate: {calc_rate}")
        print(f"   Target IPS: {config['ips_output']}")
        print(f"   Result: {result['furnace_needed']} (Expected: {expected_furnaces})")

        self.assertEqual(result["furnace_needed"], expected_furnaces)

    def test_productivity_speed_penalty(self):
        """Test 4: Productivity Modules (Speed Penalty check)"""
        print("\nRunning Test: Productivity Speed Penalty...")

        config = self.get_base_config()
        config["furnace"] = "electric"
        config["module_beacon_choice"] = "with"

        # Simulating 2x Productivity3 Modules
        # Stats from your config.py: "production3": {"speed": -0.15, "prod": 0.10}
        config["speed_stats"] = -0.30  # (-0.15 * 2)
        config["prod_stats"] = 0.20  # (0.10 * 2)

        result = calculation(config)

        # Dynamic Math Check
        base_rate = STEEL_ELECTRIC_FURNACE_BASE_RATES["iron plate"]

        # Speed modifier = 1 + (-0.30) = 0.70
        # Prod modifier  = 1 + 0.20 = 1.20
        # Final Rate = Base * 0.70 * 1.20
        calc_rate = base_rate * (1 + config["speed_stats"]) * (1 + config["prod_stats"])

        expected_furnaces = ceil(config["ips_output"] / calc_rate)

        print(f"   Base Rate: {base_rate}")
        print(f"   Adjusted Speed: {1 + config['speed_stats']} (Should be < 1)")
        print(f"   Calc Rate: {calc_rate}")

        self.assertEqual(result["furnace_needed"], expected_furnaces)

    def test_beacons(self):
        """Test 5: Beacons adding Speed"""
        print("\nRunning Test: Beacons...")

        config = self.get_base_config()
        config["furnace"] = "electric"
        config["module_beacon_choice"] = "with"

        # 8 Beacons, each with 2x Speed3
        # Speed3 = 0.5 speed. So 1 beacon = 1.0 speed.
        config["beacon_amount"] = 8
        config["beacon_speed_stats"] = 1.0

        result = calculation(config)

        # Dynamic Math Check
        base_rate = STEEL_ELECTRIC_FURNACE_BASE_RATES["iron plate"]

        # Total Speed = Machine Speed (0) + (Beacons * Beacon Speed)
        # Total Speed = 0 + (8 * 1.0) = 8.0 (+800%)
        # Multiplier = 1 + 8.0 = 9.0
        calc_rate = base_rate * 9.0

        expected_furnaces = ceil(config["ips_output"] / calc_rate)

        print(f"   Calc Rate (Super Speed): {calc_rate}")
        self.assertEqual(result["furnace_needed"], expected_furnaces)

if __name__ == '__main__':
    unittest.main()