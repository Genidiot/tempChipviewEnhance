import ParseConfig
from ParseConfig import Parser
from ParseConfig import Pin
from ParseConfig import PinDefinition
from ParseConfig import PinLayout
from ParseConfig import Point
from ParseConfig import Polygon


class Drawcell:
    def __init__(self, config: ParseConfig.Parser, dwg):
        self.dwg = dwg
        self.msp = self.dwg.modelspace()
        self.config = config

    def draw_cell(self):
        tile_name = self.config.get_device_attribute().get_name()
        width = self.config.get_graphic().width
        height = self.config.get_graphic().height

        cell_block = self.dwg.blocks.new(name=tile_name)
        points = self.config.get_graphic().get_polygon_nodes()
        cell_block.add_lwpolyline(points, close=True)

        left_pin = self.config.get_pin_layout().get_left_pin().get_multiple_pins()
        for pin in left_pin:
            name = pin.pin_name
            pin_num = pin.num
            point_start = pin.start_pos
            point_end = pin.end_pos
            step = pin.space

            x1, y1 = point_start
            x2, y2 = point_end

            x_step = (x2 - x1) / (pin_num - 1)
            y_step = (y2 - y1) / (pin_num - 1)

            for i in range(pin_num):
                x = x1 + i * x_step
                y = y1 + i * y_step
                pin_name = name + '[' + str(i) + ']'
                pin_block = self.dwg.blocks.new(name=pin_name)
                pin_block.add_circle((0, 0), 0.5)
                cell_block.add_blockref(pin_name, (x, y))


    def save_test(self, filename: str):
        self.msp.add_blockref(self.config.get_device_attribute().get_name(), (0, 0))
        self.dwg.saveas(filename=filename)

