import json
import os.path


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return


class Graphic:
    def __init__(self, graphic_type, height=None, width=None, length=None, basic_point=None, polygon_nodes=None):
        self.graphic_type = graphic_type
        self.height = height
        self.width = width
        self.length = length
        self.basic_point = basic_point
        self.polygon_nodes = polygon_nodes

    def get_basic_point(self):
        return self.basic_point

    def get_polygon_nodes(self):
        return self.polygon_nodes


class Polygon(Graphic):
    def __init__(self, height, width, basic_point, polygon_nodes):
        super().__init__('polygon', height=height, width=width, basic_point=basic_point, polygon_nodes=polygon_nodes)


class Rectangle(Graphic):
    def __init__(self, height, width, basic_point, polygon_nodes):
        super().__init__('rectangle', height=height, width=width, basic_point=basic_point, polygon_nodes=polygon_nodes)


class Line(Graphic):
    def __init__(self, length, basic_point):
        super().__init__('line', length=length, basic_point=basic_point)


# class Pin:
#     def __init__(self, pin_data):
#         self.multiple_pins = [
#             {
#                 "pinName": pin["pinName"],
#                 "direction": pin["direction"],
#                 "num": pin["num"],
#                 "space": pin["space"],
#                 "startPos": (pin["startPos"]["x"], pin["startPos"]["y"]),
#                 "endPos": (pin["endPos"]["x"], pin["endPos"]["y"])
#             } for pin in pin_data.get('multiple', [])
#         ]
#         self.single_pins = [
#             {
#                 "pinName": pin["pinName"],
#                 "pos": (pin["pos"]["x"], pin["pos"]["y"])
#             } for pin in pin_data.get('single', [])
#         ]
#
#     def get_multiple_pins(self):
#         return self.multiple_pins
#
#     def get_single_pins(self):
#         return self.single_pins

class MultiplePin:
    def __init__(self, pin_name, direction, num, space, start_pos, end_pos):
        self.pin_name = pin_name
        self.direction = direction
        self.num = num
        self.space = space
        self.start_pos = start_pos  # This will be a tuple (x, y)
        self.end_pos = end_pos  # This will be a tuple (x, y)

    def __repr__(self):
        return f"MultiplePin(pin_name={self.pin_name}, direction={self.direction}, num={self.num}, space={self.space}, start_pos={self.start_pos}, end_pos={self.end_pos})"


class SinglePin:
    def __init__(self, pin_name, pos):
        self.pin_name = pin_name
        self.pos = pos  # This will be a tuple (x, y)

    def __repr__(self):
        return f"SinglePin(pin_name={self.pin_name}, pos={self.pos})"


class Pin:
    def __init__(self, pin_data):
        self.multiple_pins = [
            MultiplePin(pin["pinName"], pin["direction"], pin["num"], pin["space"],
                        (pin["startPos"]["x"], pin["startPos"]["y"]),
                        (pin["endPos"]["x"], pin["endPos"]["y"]))
            for pin in pin_data.get('multiple', [])
        ]
        self.single_pins = [
            SinglePin(pin["pinName"], (pin["pos"]["x"], pin["pos"]["y"]))
            for pin in pin_data.get('single', [])
        ]

    def get_multiple_pins(self):
        return self.multiple_pins

    def get_single_pins(self):
        return self.single_pins

    def __repr__(self):
        return f"Pin(multiple_pins={self.multiple_pins}, single_pins={self.single_pins})"



class PinLayout:
    def __init__(self, pin_layout_data):
        self.block = pin_layout_data.get('block', '')
        self.left_pin = Pin(pin_layout_data.get('leftPin', {}))
        self.right_pin = Pin(pin_layout_data.get('rightPin', {}))
        self.down_pin = Pin(pin_layout_data.get('downPin', {}))
        self.up_pin = Pin(pin_layout_data.get('upPin', {}))

    def get_left_pin(self):
        return self.left_pin

    def get_right_pin(self):
        return self.right_pin

    def get_down_pin(self):
        return self.down_pin

    def get_up_pin(self):
        return self.up_pin


class DeviceAttribute:
    def __init__(self, attribute_data):
        self.index = attribute_data.get('index')
        self.type = attribute_data.get('type')
        self.name = attribute_data.get('name')

    def get_attributes(self):
        return {"index": self.index, "type": self.type, "name": self.name}

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type


class PinDefinition:
    def __init__(self, pin_def_data):
        self.graphic = Line(pin_def_data['length'],
                            (pin_def_data['basicPoint']['x'], pin_def_data['basicPoint']['y']))
        self.connect_points = {
            direction: (coord["x"], coord["y"])
            for direction, coord in pin_def_data['connectPoint'].items()
        }
        self.device_attribute = DeviceAttribute(pin_def_data['deviceAttribute'])

    @staticmethod
    def load_from_file(file_path):
        with open(file_path, 'r') as file:
            pin_def_data = json.load(file)
        return PinDefinition(pin_def_data)

    def get_graphic(self):
        return self.graphic

    def get_connect_points(self):
        return self.connect_points

    def get_device_attribute(self):
        return self.device_attribute


class Parser:
    def __init__(self, json_data, base_path):
        self.json_data = json_data
        self.graphic = self.parse_graphic()
        self.pin_layout = PinLayout(self.json_data.get('pinLayout', {}))
        self.device_attribute = DeviceAttribute(self.json_data.get('deviceAttribute', {}))
        self.pin_definition = self.load_pin_definition(self.pin_layout.block, base_path)

    def parse_graphic(self):
        graphic_type = self.json_data.get('graphic')
        height = self.json_data.get('height')
        width = self.json_data.get('width')
        length = self.json_data.get('length')
        basic_point = (self.json_data.get('basicPoint', {}).get('x', 0),
                       self.json_data.get('basicPoint', {}).get('y', 0))
        polygon_nodes = [(node['x'], node['y']) for node in self.json_data.get('polygonNodes', [])]

        if graphic_type == 'polygon':
            return Polygon(height, width, basic_point, polygon_nodes)
        elif graphic_type == 'rectangle':
            return Rectangle(height, width, basic_point, polygon_nodes)
        elif graphic_type == 'line':
            return Line(length, basic_point)
        else:
            raise ValueError(f"Unsupported graphic type: {graphic_type}")

    def load_pin_definition(self, block_file, base_path):
        ref_path = os.path.join(base_path, block_file)
        return PinDefinition.load_from_file(ref_path)

    def get_graphic(self):
        return self.graphic

    def get_pin_layout(self):
        return self.pin_layout

    def get_device_attribute(self):
        return self.device_attribute

    def get_pin_definition(self):
        return self.pin_definition
