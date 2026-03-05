import sys
import types
# create a dummy cte module since the real one is not available in tests
# sys.modules['cte'] = types.SimpleNamespace()
# also stub urandom (used for seeding) since standard library module isn't present
# sys.modules['urandom'] = types.SimpleNamespace(seed=lambda x: None)

import unittest
import chips
# use the Color enum defined in the fake vex module inside chips
from chips import Color

class FakeArm:
    def __init__(self):
        self.fake_location = [0, 0, 0]
        self.locations_map = []

    def move_to(self, x, y, z):
        self.fake_location = [x, y, z]
        self.locations_map.append(self.fake_location)
    
    def clear_history(self):
        self.locations_map = []
    
    def set_end_effector_magnet(self, a):
        self.locations_map.append(a)


class FakeSensor:
    def __init__(self, color_return_list):
        if len(color_return_list) == 0:
            raise Exception('cant return no value when prompted, color_return_list is empty')
        self.colors = color_return_list
        self.loop_track = 0
    
    def color(self):
        if self.loop_track == len(self.colors)-1:
            self.loop_track = 0
        return self.colors[self.loop_track]

    def is_near_object(self):
        return True

    # stubs for light control used by Chip._set_color
    def set_light(self, state):
        pass

    def set_light_power(self, power, unit):
        pass

class test_chip(unittest.TestCase):
    def test_move(self):
        arm = FakeArm()
        sensor = FakeSensor(['red_place_holder'])
        a = chips.Chip(
            arm=arm,
            sensor=sensor,
            height_of_chip=10, 
            location_of_chip=[0, 0, 0], 
            sensor_location=[30, 30, 30], 
            travel_height=200, 
            color_of_chip=None
        )

        arm.clear_history()
        a.move_to([100, 100, 0])

        ideal_map_after_move = [
            False,                    # magnet off at start
            [0, 0, 200],              # lift to travel height
            [0, 0, 20],               # approach top of chip
            [0, 0, 10],               # grab chip
            True,                     # magnet on
            [0, 0, 200],              # lift again
            [100, 100, 200],          # move above destination
            [100, 100, 20],           # approach destination
            [100, 100, 10],           # place chip
            False,                    # release magnet
            [100, 100, 200],          # retreat
        ]

        self.assertEqual(arm.locations_map, ideal_map_after_move)
    
    def test_get_color(self):
        arm = FakeArm()
        sensor = FakeSensor(['red_place_holder'])
        a = chips.Chip(
            arm=arm,
            sensor=sensor,
            height_of_chip=10, 
            location_of_chip=[0, 0, 0], 
            sensor_location=[30, 30, 30], 
            travel_height=200, 
            color_of_chip=None
        )

        arm.clear_history()
        # perform color scan; move history is validated below
        color_thought = a.get_color()
        self.assertEqual(color_thought, 'red_place_holder')

        ideal_map_after_move = [
            False,                    # initial magnet off
            [0, 0, 200],              # lift to travel height at origin
            [0, 0, 20],               # approach original chip
            [0, 0, 10],               # grab chip
            True,                     # magnet engaged
            [0, 0, 200],              # lift again
            [30, 30, 200],            # move above sensor location
            [30, 30, 60],             # approach sensor top
            [30, 30, 50],             # touch sensor
            [30, 30, 200],            # retreat from sensor
            [0, 0, 200],              # return to start above
            [0, 0, 20],               # lower back toward original spot
            [0, 0, 10],               # reposition chip
            False,                    # release magnet
            [0, 0, 200],              # final retreat
        ]

        self.assertEqual(arm.locations_map, ideal_map_after_move)


class test_stack(unittest.TestCase):
    def setUp(self):
        self.sensor_location = [36, 36, 36]
        self.travel_height = 200
        self.f_arm = FakeArm()
        self.f_sensor = FakeSensor(['red', 'green', 'blue', 'violate', 'yellow'])

        # create a handful of individual chip objects for reuse in tests
        self.test_chip_a = chips.Chip(
            arm=self.f_arm,
            sensor=self.f_sensor,
            height_of_chip=10,
            location_of_chip=[0, 0, 0],
            sensor_location=self.sensor_location,
            travel_height=self.travel_height,
            color_of_chip=None,
        )
        self.test_chip_b = chips.Chip(
            arm=self.f_arm,
            sensor=self.f_sensor,
            height_of_chip=10,
            location_of_chip=[1, 1, 0],
            sensor_location=self.sensor_location,
            travel_height=self.travel_height,
            color_of_chip=None,
        )
        self.test_chip_c = chips.Chip(
            arm=self.f_arm,
            sensor=self.f_sensor,
            height_of_chip=10,
            location_of_chip=[2, 2, 0],
            sensor_location=self.sensor_location,
            travel_height=self.travel_height,
            color_of_chip=None,
        )
        self.test_chip_d = chips.Chip(
            arm=self.f_arm,
            sensor=self.f_sensor,
            height_of_chip=10,
            location_of_chip=[3, 3, 0],
            sensor_location=self.sensor_location,
            travel_height=self.travel_height,
            color_of_chip=None,
        )

        # make list small and predictable
        self.list_of_chips = [
            self.test_chip_a,
            self.test_chip_b,
            self.test_chip_c,
            self.test_chip_d,
        ]

        self.f_arm.clear_history()

    def test_init(self):
        self.f_arm.clear_history()
        stk = chips.Stack(
            arm=self.f_arm,
            sensor=self.f_sensor,
            chip_height=10,
            origin_chip=[0, 0, 0],
            amount_stacked=5,
        )

        self.assertEqual(len(stk.chips), 5)

        chip_locations = [i.current_location for i in stk.chips]
        expectation = [[0, 0, i*10] for i in range(5)]

        for test_loc, expected_loc in zip(chip_locations, expectation):
            self.assertEqual(test_loc, expected_loc)

    def test_StackBuilderObjects(self):
        self.f_arm.clear_history()
        stk = chips.Stack.StackBuilderObjects(
            arm=self.f_arm,
            sensor=self.f_sensor,
            chip_height=10,
            chip_objects=self.list_of_chips,
            destination=[40, 40, 0],
            move=True
        )

        chip_locations = [i.current_location for i in stk.chips]
        expectation = [[40, 40, idx*10] for idx in range(len(self.list_of_chips))]
        for test_loc, expected_loc in zip(chip_locations, expectation):
            self.assertEqual(test_loc, expected_loc)

    def test_StackBuilderCords(self):
        self.f_arm.clear_history()
        stk = chips.Stack.StackBuilderCords(
            arm=self.f_arm,
            sensor=self.f_sensor,
            chip_height=10,
            chip_cords=[i.current_location for i in self.list_of_chips],
            destination=[45, 45, 0],
            move=True
        )

        chip_locations = [i.current_location for i in stk.chips]
        expectation = [[45, 45, idx*10] for idx in range(len(self.list_of_chips))]
        for test_loc, expected_loc in zip(chip_locations, expectation):
            self.assertEqual(test_loc, expected_loc)

    def test_unstack(self):
        stk = chips.Stack(
            arm=self.f_arm,
            sensor=self.f_sensor,
            chip_height=10,
            origin_chip=[10, 10, 0],
            amount_stacked=3,
        )
        destinations = [[0,0,0],[1,1,0],[2,2,0]]

        removed = stk.unstack(destinations)
        # we should get 3 chips and they should have been moved to the provided
        # coordinates
        self.assertEqual([c.current_location for c in removed], destinations)
        # remaining stack should be empty
        self.assertEqual(stk.chips, [])

    def test_move_to(self):
        self.f_arm.clear_history()
        stk = chips.Stack.StackBuilderObjects(
            arm=self.f_arm,
            sensor=self.f_sensor,
            chip_height=10,
            chip_objects=self.list_of_chips,
            destination=[45, 45, 0],
            move=True
        )

        original_order = stk.chips.copy()
        stk.move_to([70, 70, 0])

        # after moving the order should be reversed
        self.assertEqual(stk.chips, original_order[::-1])
        # the z locations should all be relative to new base
        for idx, chip in enumerate(stk.chips):
            self.assertEqual(chip.current_location, [70,70, idx*10])

    def test_sort(self):
        # create a small stack with predictable colors
        a = chips.Chip(self.f_arm, self.f_sensor, 10, [0,0,0])
        b = chips.Chip(self.f_arm, self.f_sensor, 10, [1,0,0])
        c = chips.Chip(self.f_arm, self.f_sensor, 10, [2,0,0])
        # manually set colors to avoid sensor movement
        a.color_of_chip = Color.RED
        b.color_of_chip = Color.GREEN
        c.color_of_chip = Color.BLUE
        stk = chips.Stack(self.f_arm, self.f_sensor, 10, [5,5,0], 0)
        stk.chips = [a,b,c]  # bottom->top

        piles = stk.sort(key=[
            [lambda ch: ch.color_of_chip==Color.GREEN, [10,10,0]],
            [lambda ch: ch.color_of_chip==Color.RED, [20,20,0]],
            [lambda ch: True, [30,30,0]],
        ])
        # green chip should end up in first pile, red in second, blue in else
        self.assertEqual(len(piles[(10,10,0)].chips), 1)
        self.assertEqual(piles[(10,10,0)].chips[0].color_of_chip, Color.GREEN)
        self.assertEqual(len(piles[(20,20,0)].chips), 1)
        self.assertEqual(piles[(20,20,0)].chips[0].color_of_chip, Color.RED)
        self.assertEqual(len(piles[(30,30,0)].chips), 1)
        self.assertEqual(piles[(30,30,0)].chips[0].color_of_chip, Color.BLUE)

    def test_update_colors(self):
        # build a tiny stack; fake sensor will cycle through colors
        stk = chips.Stack.StackBuilderObjects(
            arm=self.f_arm,
            sensor=self.f_sensor,
            chip_height=10,
            chip_objects=[self.test_chip_a, self.test_chip_b],
            destination=[0,0,0],
            move=False
        )
        # reset fake arm history to capture moves
        self.f_arm.clear_history()
        stk.update_colors([50,50,0])
        # after update_colors, both chips should report a color from fake sensor
        for chip in stk.chips:
            self.assertIsNotNone(chip.color_of_chip)
        # order should be inverted
        self.assertEqual(stk.chips, [self.test_chip_b, self.test_chip_a])


if __name__ == '__main__':
    unittest.main()
