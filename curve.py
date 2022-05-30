# BeanieTools: Curve Creator
# 5/29/2022

import argparse
from curve_classes import Position, Curve
from curve_methods_main import modify_ksh

parser = argparse.ArgumentParser(description='Generate a curve.')
parser.add_argument('filename', help='the ksh filename (string)')
parser.add_argument('-o', '--overwrite', action='store_true', help='for overwriting existing ksh file')
parser.add_argument('start_measure_number', type=int, help='start measure number (int)')
parser.add_argument('start_note_num', type=int, help='start note numerator (int)')
parser.add_argument('start_note_den', type=int, help='start note denominator (int)')
parser.add_argument('end_measure_number', type=int, help='end measure number (int)')
parser.add_argument('end_note_num', type=int, help='end note numerator (int)')
parser.add_argument('end_note_den', type=int, help='end note denominator (int)')
parser.add_argument('laser_color', metavar='laser_color', choices=['B', 'R'], default=1, help='\'B\' for Blue, \'R\' for Red')
parser.add_argument('-w', '--wide', action='store_true', help='for wide lasers')
parser.add_argument('laser_start_loc', help='laser start location (char)')
parser.add_argument('laser_end_loc', help='laser end location (char)')
parser.add_argument('curvature', type=float, help='curvature of laser (float)')
parser.add_argument('-e', '--erase', action='store_true', help='for erasing existing laser; ignores laser locations, curvature, -w/--wide')

args = parser.parse_args()

# EXECUTION
output_name = modify_ksh(args.filename,
	Position(args.start_measure_number, args.start_note_num, args.start_note_den),
	Position(args.end_measure_number, args.end_note_num, args.end_note_den), 
	Curve(args.laser_color, str.encode(args.laser_start_loc), str.encode(args.laser_end_loc), args.curvature, args.wide),
	args.erase, args.overwrite)

if not args.erase:
	print('Curve generated in file ' + output_name)
else:
	print('Curve erased in file ' + output_name)
