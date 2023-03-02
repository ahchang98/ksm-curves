# BeanieTools: Curve Creator

import argparse, re
from curve_classes import Position, Curve
from curve_methods_main import modify_ksh

parser = argparse.ArgumentParser(description='Generate a curve.')
parser.add_argument('filename', help='string = the ksh filename')
parser.add_argument('start_data', help='int:int/int = start measure number : note numerator / denominator ')
parser.add_argument('end_data', help='int:int/int = end measure number : note numerator / denominator ')
parser.add_argument('laser_data', help='x:char-char = laser color B or R : start - end')
parser.add_argument('laser_curvature', nargs='?', default=argparse.SUPPRESS, help='float = laser curvature')

parser.add_argument('-w', '--wide', action='store_true', help='for wide lasers')
parser.add_argument('-o', '--overwrite', action='store_true', help='for overwriting existing ksh file')
parser.add_argument('-e', '--erase', action='store_true', help='for erasing existing laser; curvature ignored')

args = parser.parse_args()

start_split = re.split(r'[:/]', args.start_data)
start_measure_number = int(start_split[0])
start_note_num = int(start_split[1])
start_note_den = int(start_split[2])

end_split = re.split(r'[:/]', args.end_data)
end_measure_number = int(end_split[0])
end_note_num = int(end_split[1])
end_note_den = int(end_split[2])

laser_split = re.split(r'[:\-]', args.laser_data)
laser_color = laser_split[0]

if not args.erase:
	laser_start_loc = str.encode(laser_split[1])
	laser_end_loc = str.encode(laser_split[2])
	curvature = float(args.laser_curvature)

	output_name = modify_ksh(args.filename,
		Position(start_measure_number, start_note_num, start_note_den),
		Position(end_measure_number, end_note_num, end_note_den),
		Curve(laser_color, laser_start_loc, laser_end_loc, curvature, args.wide),
		args.erase, args.overwrite)

	print('Curve generated in file ' + output_name)
else:
	output_name = modify_ksh(args.filename,
		Position(start_measure_number, start_note_num, start_note_den),
		Position(end_measure_number, end_note_num, end_note_den),
		Curve(laser_color, b'0', b'0', 0, args.wide),
		args.erase, args.overwrite)

	print('Curve erased in file ' + output_name)
