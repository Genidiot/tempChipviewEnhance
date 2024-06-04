# This is a sample Python script.
import os.path
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import json
import ezdxf
import random
import sys
import pygame
import math

import DrawCell
from DrawCell import Drawcell
import ParseConfig
from ParseConfig import Parser

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_file_path = f'./config/cla_def.json'
    with open(main_file_path, 'r') as cla_def_json:
        cla_def_data = json.load(cla_def_json)

    base_path = os.path.dirname(main_file_path)
    cla_def_parser = Parser(cla_def_data, base_path)

    # points = [(0, 12), (2, 36)]
    # point = (5, 28)
    #
    # # 解析后的数据结构可以通过接口函数进行访问，例如：
    # print(cla_def_parser.get_graphic().graphic_type)
    # print(cla_def_parser.get_pin_layout().get_left_pin().get_multiple_pins())
    # print(cla_def_parser.get_device_attribute().get_attributes())
    # print(cla_def_parser.get_pin_definition().get_graphic().graphic_type)
    # print(cla_def_parser.get_pin_definition().get_connect_points())
    # print(cla_def_parser.get_graphic().polygon_nodes)
    # print(points)
    # print(point)

    dxf_test = ezdxf.new(dxfversion='AC1021')
    cla_ = DrawCell.Drawcell(cla_def_parser, dxf_test)
    cla_.draw_cell()
    cla_.save_test(f"cla.dxf")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
