# BeanieTools: Curve Creator
# 5/29/2022

import math, re

LASER_LOCATIONS = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmno'

# Curve methods
def find_length(measures, start_position, end_position):
	if start_position.measure_index == end_position.measure_index:
		current_beat = find_current_beat(measures, start_position)
		return convert_position_to_point(current_beat, end_position) - convert_position_to_point(current_beat, start_position)
	
	length = 0

	measure_index = start_position.measure_index
	current_beat = find_current_beat(measures, start_position)
	points_data = calculate_points_data(measures[measure_index], current_beat)
	length += points_data[1] - convert_position_to_point(current_beat, start_position)

	measure_index += 1
	while measure_index < end_position.measure_index:
		current_beat = update_beat(measures[measure_index], current_beat)
		points_data = calculate_points_data(measures[measure_index], current_beat)
		length += points_data[1]
		measure_index += 1

	current_beat = update_beat(measures[measure_index], current_beat)
	length += convert_position_to_point(current_beat, end_position)

	return length

def calculate_curve_string(curve_data, length):
	start_index = convert_location_to_index(curve_data.start)
	end_index = convert_location_to_index(curve_data.end)

	curve_string = curve_data.start
	previous_increment = 0
	continuation_count = 0
	for i in range(length - 1):
		if start_index > end_index:
			new_increment = math.floor((end_index - start_index) * math.pow(i / length, math.pow(1.1, curve_data.curvature)))
		else:
			new_increment = math.floor((end_index - start_index) * math.pow(i / length, math.pow(1.1, -1 * curve_data.curvature)))
		
		new_index = start_index + new_increment
		if i < (length - 7) and abs(new_increment - previous_increment) > 0 and continuation_count >= 6:
			curve_string += LASER_LOCATIONS[new_index:new_index + 1]
			previous_increment = new_increment
			continuation_count = 0
		else:
			curve_string += b':'
			continuation_count += 1

	curve_string += curve_data.end
	return curve_string

# Measure methods
def split_measure(measure):
	return measure.split(b'\r\n')

def join_measure(measure_lines):
	return b'\r\n'.join(measure_lines)

def expand_measure(measure, beat):
	measure_lines = split_measure(measure)
	points_data = calculate_points_data(measure, beat)
	
	new_measure_lines = []
	for line in measure_lines:
		new_measure_lines.append(line)
		if is_a_point(line):
			for i in range(points_data[2] - 1):
				new_measure_lines.append(b'0000|00|--')
	
	new_measure = join_measure(new_measure_lines)
	return new_measure

# Beat methods
def find_beat(measure):
	measure_lines = split_measure(measure)

	beat_pattern = re.compile(b'beat=')
	for line in measure_lines:
		if beat_pattern.match(line):
			beat_string = line.removeprefix(b'beat=')
			beat_split = beat_string.split(b'/')
			return (int(beat_split[0]), int(beat_split[1]))

	return None

def find_current_beat(measures, start_position):
	current_beat = None
	beat_index = start_position.measure_index + 1
	while not current_beat:
		beat_index -= 1
		current_beat = find_beat(measures[beat_index])

	return current_beat

def update_beat(measure, old_beat):
	new_beat = find_beat(measure)
	if new_beat:
		return new_beat
	return old_beat

# Point methods
def count_points(measure):
	measure_lines = split_measure(measure)

	points = 0
	for line in measure_lines:
		if is_a_point(line):
			points += 1

	return points

def calculate_points_data(measure, beat):
	old_points_in_measure = count_points(measure)
	max_points_in_measure = int(192 * (beat[0] / beat[1]))
	ratio = int(max_points_in_measure / old_points_in_measure)

	return (old_points_in_measure, max_points_in_measure, ratio)

def is_a_point(measure_line):
	point_pattern = re.compile(b'[012]{4}\|[012]{2}\|..')
	return point_pattern.match(measure_line)

# Conversion methods
def convert_position_to_line(measures, position):
	beat = find_current_beat(measures, position)
	points_data = calculate_points_data(measures[position.measure_index], beat)
	measure_lines = split_measure(measures[position.measure_index])
	
	point_goal = int(192 * ((position.numerator - 1) / position.denominator))
	point_count = 0
	line_index = 0

	if point_goal == 0:
		while not is_a_point(measure_lines[line_index]):
			line_index += 1

	while point_count < point_goal:
		if is_a_point(measure_lines[line_index]):
			point_count += 1
		line_index += 1

	return line_index

def convert_position_to_point(beat, position):
	max_points = int(192 * (beat[0] / beat[1]))
	position_ratio = (position.numerator - 1) / position.denominator
	return int(max_points * position_ratio) + 1

def convert_location_to_index(location):
	return LASER_LOCATIONS.index(location)
