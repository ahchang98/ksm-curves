# BeanieTools: Curve Creator

import math, re
from curve_classes import Beat

LASER_LOCATIONS = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmno'
LASER_SPACING = 8

# Curve methods
def calculate_curve_bytes(measures, start_position, end_position, curve_data):
	length = calculate_curve_length(measures, start_position, end_position)
	start_index = convert_location_to_index(curve_data.start)
	end_index = convert_location_to_index(curve_data.end)

	curve_bytes = curve_data.start

	continuation_count = 0
	for i in range(length - 1):
		if curve_data.curvature > 0:
			increment = abs(end_index - start_index) - math.floor(abs(end_index - start_index) * math.pow((length - i)/length, math.pow(2, curve_data.curvature)))
		else:
			increment = math.floor(abs(end_index - start_index) * math.pow(i/length, math.pow(2, -1 * curve_data.curvature)))

		if start_index > end_index:
			increment *= -1

		if continuation_count >= LASER_SPACING - 1 and i < (length - LASER_SPACING):
			new_index = start_index + increment
			curve_bytes += LASER_LOCATIONS[new_index:new_index + 1]
			continuation_count = 0
		else:
			curve_bytes += b':'
			continuation_count += 1

	curve_bytes += curve_data.end

	return curve_bytes

def calculate_curve_length(measures, start_position, end_position):
	if start_position.measure_index == end_position.measure_index:
		current_beat = find_current_beat(measures, start_position)
		return convert_position_to_point(current_beat, end_position) - convert_position_to_point(current_beat, start_position)
	
	length = 0

	measure_index = start_position.measure_index
	current_beat = find_current_beat(measures, start_position)
	length += calculuate_max_points_in_measure(current_beat) - convert_position_to_point(current_beat, start_position)

	while measure_index < end_position.measure_index - 1:
		measure_index += 1
		current_beat = update_beat(measures[measure_index], current_beat)
		length += calculuate_max_points_in_measure(current_beat)

	measure_index += 1
	current_beat = update_beat(measures[measure_index], current_beat)
	length += convert_position_to_point(current_beat, end_position)

	return length

# Measure methods
def split_measure(measure):
	return measure.split(b'\r\n')

def join_measure(measure_lines):
	return b'\r\n'.join(measure_lines)

def expand_measure(measure, beat):
	ratio = int(calculuate_max_points_in_measure(beat) / count_points(measure))
	measure_lines = split_measure(measure)

	new_measure_lines = []
	for line in measure_lines:
		new_measure_lines.append(line)
		if is_a_point(line):
			template_line = b''

			for bt in range(4):
				if line[bt:bt + 1] == b'2':
					template_line += b'2'
				else:
					template_line += b'0'

			template_line += b'|'

			for fx in range(2):
				if line[(5 + fx):(6 + fx)] == b'1':
					template_line += b'1'
				else:
					template_line += b'0'

			template_line += b'|'

			for vol in range(2):
				if line[(8 + vol):(9 + vol)] != b'-':
					template_line += b':'
				else:
					template_line += b'-'

			for i in range(ratio - 1):
				new_measure_lines.append(template_line)
	
	new_measure = join_measure(new_measure_lines)
	return new_measure

# Beat methods
def find_beat_in_measure(measure):
	measure_lines = split_measure(measure)

	beat_pattern = re.compile(b'beat=')
	for line in measure_lines:
		if beat_pattern.match(line):
			beat_string = line.removeprefix(b'beat=')
			beat_split = beat_string.split(b'/')
			return Beat(int(beat_split[0]), int(beat_split[1]))

	return None

def find_current_beat(measures, start_position):
	current_beat = None
	beat_index = start_position.measure_index + 1
	while not current_beat:
		beat_index -= 1
		current_beat = find_beat_in_measure(measures[beat_index])

	return current_beat

def update_beat(measure, old_beat):
	new_beat = find_beat_in_measure(measure)
	if new_beat:
		return new_beat
	return old_beat

# Point methods
def is_a_point(measure_line):
	point_pattern = re.compile(b'[012]{4}\|[012]{2}\|...*')
	return point_pattern.match(measure_line)

def count_points(measure):
	measure_lines = split_measure(measure)

	points = 0
	for line in measure_lines:
		if is_a_point(line):
			points += 1

	return points

def calculuate_max_points_in_measure(beat):
	return int(192 * (beat.top / beat.bottom))

# Conversion methods
def convert_position_to_line(measure, position):
	measure_lines = split_measure(measure)
	
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
	max_points_in_measure = calculuate_max_points_in_measure(beat)
	position_ratio = (position.numerator - 1) / position.denominator
	return int(max_points_in_measure * position_ratio)

def convert_location_to_index(location):
	return LASER_LOCATIONS.index(location)
