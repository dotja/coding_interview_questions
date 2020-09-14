import os
import sys
import argparse
import logging
import csv
import numpy

class Interpolator:
	"""
	Used to generate interpolated data of N/A values by averaging the neighboring and non-diagonal values.
	Arguments:
		in_csv  = a CSV file that has the N/A values as 'nan'.
		out_csv = to be written to. The matrix with N/A occurrences replaced by interpolated values.
	"""
	def __init__(self, in_csv, out_csv, logger):
		self.logger = logger
		self.in_csv = in_csv
		self.out_csv = out_csv
		self._csv_check()
	##--------------------------------------
	def _csv_check(self):
		"""
		Validates that the input CSV exists.
		Validates that the output CSV is not a non-empty existing file.
		"""
		if not os.path.exists(in_csv):
			self.logger.error('Can not find file: {0}'.format(in_csv))
			sys.exit('Exiting.')
		##
		if os.path.exists(out_csv) and not os.path.getsize(out_csv) == 0:
			self.logger.info('The output file is not empty: {0}'.format(out_csv))
			answer = input('Do you want to continue and override it?(y/n) => ')
			if answer == 'y':
				pass
			elif answer == 'n':
				sys.exit('Exiting script.')
			else:
				sys.exit('Did not recognise your response. Exiting script.')
		##
		try:
			file_reader = csv.reader(open(in_csv, 'r'), delimiter=',')
			self.matrix = numpy.array(list(file_reader))
		except IOError:
			self.logger.error('Unable to properly read the CSV file {0}', in_csv)
			sys.exit('Exiting.')
		##
		self.dims = self.matrix.shape
		self.result = numpy.array(self.matrix, copy=True)
	##--------------------------------------
	def _find_nan_indices(self):
		"""
		Finds the indices of N/A values.
		"""
		self.nan_indices = [(x,y) for x,y in zip(*numpy.where(self.matrix=='nan'))]
		return
	##--------------------------------------
	def _find_diag_indices(self):
		"""
		Finds the diagonal indices in the matrix.
		"""
		diag_indices_array = numpy.diag_indices(self.dims[0]-1)
		self.diag_indices = [(n,m) for n,m in zip(*diag_indices_array)]
		return
	##--------------------------------------
	def _valid_neighbor_coord(self, x, y):
		"""
		Determines the valid neighboring coordinates of a location.
		"""
		valid_coords = []
		if x-1 >= 0:
			valid_coords.append((x-1, y))
		if x+1 < self.dims[0]:
			valid_coords.append((x+1, y))
		if y+1 < self.dims[1]:
			valid_coords.append((x, y+1))
		if y-1 >= 0:
			valid_coords.append((x, y-1))
		return valid_coords
	##--------------------------------------
	def process_nan(self, nan_coord):
		x,y = nan_coord
		neighbors = self._valid_neighbor_coord(x, y)
		## check that neighboring index is not in diagonal indices
		neighbors = [(a,b) for (a,b) in neighbors if (a,b) not in self.diag_indices]
		## TODO: check that the value is not NAN
		## TODO: check that there is at least 1 value in the list ot use a fallback value
		interplolated_value = numpy.average([float(self.matrix[a,b]) for (a,b) in neighbors])
		return interplolated_value
	##--------------------------------------
	def generate_interpolated_data(self):
		self._find_nan_indices()
		self._find_diag_indices()
		try:
			for nan in self.nan_indices:
				interpolated_value = self.process_nan(nan)
				self.result[nan] = interpolated_value
			with open(out_csv, 'w') as out_file:
				out_file.write('\n'.join([','.join(row) for row in self.result]))
			self.logger.info('Finished processing data.')
		except:
			self.logger.error('Something went wrong.')




if __name__ == '__main__':
	##--------------------------------------
	## Parse the command-line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--csv_file_input', help='The CSV file containing your data')
	parser.add_argument('-o', '--csv_file_output', help='A name for the CSV file output generated')
	args = parser.parse_args()
	parser.set_defaults(test_run=False)
	##--------------------------------------
	## Set up the logger
	logger = logging.getLogger('logger')
	formatter = logging.Formatter('[%(levelname)s] %(message)s')
	handler = logging.StreamHandler(stream=sys.stdout)
	handler.setFormatter(formatter)
	handler.setLevel(logging.DEBUG)
	logger.addHandler(handler)
	logger.setLevel(logging.DEBUG)
	##--------------------------------------
	## Run
	in_csv = args.csv_file_input
	out_csv = args.csv_file_output
	##
	interpolator = Interpolator(in_csv, out_csv, logger)
	interpolator.generate_interpolated_data()

