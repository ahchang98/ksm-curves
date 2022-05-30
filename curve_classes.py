# BeanieTools: Curve Creator
# 5/29/2022

class Position:
	def __init__(self, input_measure, input_numerator, input_denominator):
		self.measure_index = input_measure - 1
		self.numerator = input_numerator
		self.denominator = input_denominator

class Curve:
	def __init__(self, input_color, input_start, input_end, input_curvature, wide_flag):
		self.color = input_color
		self.start = input_start
		self.end = input_end
		self.curvature = input_curvature
		self.wide = wide_flag
