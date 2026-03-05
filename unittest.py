import unittest
import chips

class FakeArm:
    def __init__(self):
        self.fake_location = [0, 0, 0]
        self.locations_map = []

    def move_to(self, x, y, z):
        self.fake_location = [x, y, z]
        self.locations_map.append(self.fake_location)
    
    def clear_history(self):
        self.locations_map = []
    
    def set_end_effector_magnet(a):
        self.locations_map.append(a)


class FakeSensor:
    def __init__(color_return_list):
        if len(color_return_list) == 0:
            raise Exception('cant return no value when prompted, color_return_list is empty')
        self.colors = color_return_list
        self.loop_track
    
    def color(self):
        if self.loop_track == len(self.colors)-1:
            self.loop_track = 0
        return self.colors[self.loop_track]


    def is_near_object(self):
        return True

class test_chip(unittest.TestCase):
    def test_move(self):
        arm = FakeArm()
        sensor = FakeSensor(['red_place_holder'])
        a = chips.chip(
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
            [0, 0, 200],
            [0, 0, 20],
            [0, 0, 10],
            True,
            [100, 100, 200],
            [100, 100, 20],
            [100, 100, 10],
            False,
            [100, 100, 200]
        ]

        self.assertEqual(arm.locations_map, ideal_map_after_move)
    
    def test_get_color(self):
        arm = FakeArm()
        sensor = FakeSensor(['red_place_holder'])
        a = chips.chip(
            arm=arm,
            sensor=sensor,
            height_of_chip=10, 
            location_of_chip=[0, 0, 0], 
            sensor_location=[30, 30, 30], 
            travel_height=200, 
            color_of_chip=None
        )

        arm.clear_history()
        color_thought = a.get_color()

        self.assertEqual(color_thought, 'red_place_holder')

        ideal_map_after_move = [
            [0, 0, 200],
            [0, 0, 20],
            [0, 0, 10],
            True,
            [30, 30, 200],
            [30, 30, 20],
            [30, 30, 10],
            [30, 30, 200],
            [0, 0, 200],
            [0, 0, 20],
            [0, 0, 10],
            False,
            [0, 0, 200]
        ]

        self.assertEqual(arm.locations_map, ideal_map_after_move)


class test_stack(unittest.TestCase):
    def setUp(self):
        self.sensor_location = [36, 36, 36]
        self.travel_height = 200
        self.f_arm = FakeArm()
        self.f_sensor = FakeSensor(['red', 'green', 'blue', 'violate', 'yellow'])

        self.test_chip_a = chips.chip(
            arm=self.f_arm,
            sensor=self.f_sensor,
            height_of_chip=10, 
            location_of_chip=[0, 0, 0], 
            sensor_location=self.sensor_location, 
            travel_height=self.travel_height, 
            color_of_chip=None
        )
        self.test_chip_b = chips.chip(
            arm=self.f_arm,
            sensor=self.f_sensor,
            height_of_chip=10, 
            location_of_chip=[0, 0, 0], 
            sensor_location=self.sensor_location, 
            travel_height=self.travel_height, 
            color_of_chip=None
        )
        self.test_chip_c = chips.chip(
            arm=self.f_arm,
            sensor=self.f_sensor,
            height_of_chip=10, 
            location_of_chip=[0, 0, 0], 
            sensor_location=self.sensor_location, 
            travel_height=self.travel_height, 
            color_of_chip=None
        )
        self.test_chip_d = chips.chip(
            arm=self.f_arm,
            sensor=self.f_sensor,
            height_of_chip=10, 
            location_of_chip=[0, 0, 0], 
            sensor_location=self.sensor_location, 
            travel_height=self.travel_height, 
            color_of_chip=None
        )
        self.test_chip_e = chips.chip(
            arm=self.f_arm,
            sensor=self.f_sensor,
            height_of_chip=10, 
            location_of_chip=[0, 0, 0], 
            sensor_location=self.sensor_location, 
            travel_height=self.travel_height, 
            color_of_chip=None
        )
        self.test_chip_f = chips.chip(
            arm=self.f_arm,
            sensor=self.f_sensor,
            height_of_chip=10, 
            location_of_chip=[0, 0, 0], 
            sensor_location=self.sensor_location, 
            travel_height=self.travel_height, 
            color_of_chip=None
        )
        self.test_chip_g = chips.chip(
            arm=self.f_arm,
            sensor=self.f_sensor,
            height_of_chip=10, 
            location_of_chip=[0, 0, 0], 
            sensor_location=self.sensor_location, 
            travel_height=self.travel_height, 
            color_of_chip=None
        )
        self.test_chip_h = chips.chip(
            arm=self.f_arm,
            sensor=self.f_sensor,
            height_of_chip=10, 
            location_of_chip=[0, 0, 0], 
            sensor_location=self.sensor_location, 
            travel_height=self.travel_height, 
            color_of_chip=None
        )

    def test_init(self):
        stk = chips.Stack(
            arm=self.arm,
            sensor=self.sensor,
            chip_height=10,
            origin_chip=[0, 0, 0],
            amount_stacked=7,
        )

        self.assertEqual(len(stk.chips), 7)

        chip_locations = [i.current_locaiton for i in stk.chips]
        expectaion = [[0, 0, i*10] for i in range(7)]

        for test, key in zip(chip_locations, expectaion):
            self.assertEqual(test, key)

    def test_StackBuilderObjects(self):
        pass

    def test_StackBuilderCords(self):
        pass

    def test_unstack(self):
        pass

    def test_move_to(self):
        pass

    def test_sort(self):
        pass

    def test_update_colors(self):
        pass


if __name__ == '__main__':
    unittest.main()