# BeanieTools: Curve Creator
# 5/29/2022

from curve_methods_aux import *

def modify_ksh(input_ksh, start_position, end_position, curve_data, erase_flag, overwrite_flag):
	with open(input_ksh, 'rb') as input_file:
		data = input_file.read()
		raw_split = data.split(b'\r\n--\r\n')
		metadata = raw_split[0]
		measures = raw_split[1:-1]
		end_data = raw_split[-1]

		modify_measures(measures, start_position, end_position, curve_data, erase_flag)

		if overwrite_flag:
			output_ksh = input_ksh
		else:
			output_ksh = input_ksh.removesuffix('.ksh') + '_CURVED.ksh'

		with open(output_ksh, 'wb') as output_file:
			output_file.write(metadata + b'\r\n--\r\n')
			for measure in measures:
				output_file.write(measure + b'\r\n--\r\n')
			output_file.write(end_data)

	return output_ksh

def modify_measures(measures, start_position, end_position, curve_data, erase_flag):
	end_difference = end_position.measure_index - len(measures) + 1
	if end_difference > 0:
		for i in range(end_difference):
			measures.append(b'0000|00|--')

	curve_length = find_length(measures, start_position, end_position)
	curve_string = calculate_curve_string(curve_data, curve_length)

	curve_index = 0
	current_beat = find_current_beat(measures, start_position)
	measure_index = start_position.measure_index
	points_data = calculate_points_data(measures[measure_index], current_beat)
	
	first_measure = True
	while curve_index < len(curve_string):
		current_measure = measures[measure_index]
		current_beat = update_beat(current_measure, current_beat)
		current_measure = expand_measure(current_measure, current_beat)
		measure_lines = split_measure(current_measure)
		measures[measure_index] = current_measure

		if first_measure:
			line_index = convert_position_to_line(measures, start_position)
		else:
			line_index = 0
		
		if curve_data.wide and first_measure:
			if curve_data.color == 'B':
				measure_lines.insert(line_index, b'laserrange_l=2x')
			elif curve_data.color == 'R':
				measure_lines.insert(line_index, b'laserrange_r=2x')
			line_index += 1
		
		while line_index < len(measure_lines):
			line = measure_lines[line_index]
			if curve_index < len(curve_string) and is_a_point(line):
				if not erase_flag:
					if curve_data.color == 'B':
						line = line[:8] + curve_string[curve_index:curve_index+1] + line[9:]
					elif curve_data.color == 'R':
						line = line[:9] + curve_string[curve_index:curve_index+1] + line[10:]
				else:
					if curve_data.color == 'B':
						line = line[:8] + b'-' + line[9:]
					elif curve_data.color == 'R':
						line = line[:9] + b'-' + line[10:]
				curve_index += 1
			measure_lines[line_index] = line
			line_index += 1
		
		current_measure = join_measure(measure_lines)
		measures[measure_index] = current_measure
		measure_index += 1
		first_measure = False
