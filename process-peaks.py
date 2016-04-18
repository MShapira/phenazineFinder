from os import listdir
from os.path import isfile, join
from numpy import genfromtxt, dtype, empty, bytes_, str_, float64, savetxt, sum


# function that processes list of lines (from range) and returns array of peaks (used to load peaks for some energy level in database files)
def load_peaks_for_energy(all_lines, start_index, peaks_number):
	# 1. create empty array
	peaks = empty(peaks_number, dtype=[('m/z', float64, 1), ('total intensity', float64, 1), ('formulas numbers', str_, 30), ('per-component intensities', str_, 90)])
	
	# 2. fill array line by line
	for i in range(0, peaks_number):
		# 2.1 split line
		components = all_lines[start_index + i].split(' ')

		# 2.2 store 'm/z'
		peaks['m/z'][i] = float(components[0])

		# 2.3 store 'total intensity'
		peaks['total intensity'][i] = float(components[1])

		# 2.4 accumulate numbers of formulas (while not found component starting with '(')
		formulas_numbers = ''
		index = 2
		while not components[index][0] == '(':
			formulas_numbers = formulas_numbers + components[index] + ' '
			index = index + 1
		formulas_numbers = formulas_numbers[:-1] # remove useless ' ' at the end

		# 2.5 store 'formulas numbers'
		peaks['formulas numbers'][i] = formulas_numbers

		# 2.6 accumulate per-component intensities
		per_component_intensities = components[index][1:] + ' ' # store first number and remove its starting '(' symbol
		index = index + 1
		while not index == len(components):
			per_component_intensities = per_component_intensities + components[index] + ' '
			index = index + 1
		per_component_intensities = per_component_intensities[:-2] # remove useless ') ' at the end

		# 2.7 store 'per-component intensities'
		peaks['per-component intensities'][i] = per_component_intensities

	# 3. sort array by 'total intensity' and return it in reversed order
	peaks.sort(order='total intensity')
	return peaks[::-1]


# function that processes list of lines (from range) and returns array of formulas (to load formulas in database file)
def load_formulas(all_lines, start_index, formulas_number):
	# 1. create empty array
	formulas = empty(formulas_number, dtype=[('mass', float64, 1), ('formula', str_, 90)])

	# 2. fill array line by line
	for i in range(0, formulas_number):
		# 2.1 split line
		components = all_lines[start_index + i].split(' ')

		# 2.2 store 'mass'
		formulas['mass'][i] = float(components[1])

		# 2.3 store 'formula'
		formulas['formula'][i] = components[2]

	# 3. return
	return formulas 


# load all files from database directory into one smart array
def load_database(directory):
	# 1. get list of file names in directory
	file_names = [f for f in listdir(directory) if isfile(join(directory, f))]

	# 2. fill database
	database = []
	for file_name in file_names:
		# 2.1 store phenazine name in record
		database_record = {'name': file_name}

		# 2.2 read file into temporary object
		all_lines = []
		with open(join(directory, file_name), 'r') as file:
			all_lines = [line[:-1] for line in file.readlines()]
		
		# 2.3 determine number of peaks for energy0
		start_index = 1 # because line #0 contains word 'energy0'
		peaks_number = 0
		while not all_lines[start_index + peaks_number][0:6] == 'energy':
			peaks_number = peaks_number + 1
		
		# 2.4 read peaks for energy0 and store them in record
		energy0 = load_peaks_for_energy(all_lines, start_index, peaks_number)
		database_record['energy0'] = energy0

		# 2.5 determine number of peaks for energy1
		start_index = start_index + peaks_number + 1
		peaks_number = 0
		while not all_lines[start_index + peaks_number][0:6] == 'energy':
			peaks_number = peaks_number + 1

		# 2.6 read peaks for energy1 and store them in record
		energy1 = load_peaks_for_energy(all_lines, start_index, peaks_number)
		database_record['energy1'] = energy1

		# 2.7 determine number of peaks for energy2
		start_index = start_index + peaks_number + 1
		peaks_number = 0
		while not all_lines[start_index + peaks_number] == '':
			peaks_number = peaks_number + 1

		# 2.8 read peaks for energy2 and store them in record
		energy2 = load_peaks_for_energy(all_lines, start_index, peaks_number)
		database_record['energy2'] = energy2

		# 2.9 load formulas and store them in record
		start_index = start_index + peaks_number + 1
		formulas_number = len(all_lines) - start_index
		formulas = load_formulas(all_lines, start_index, formulas_number)
		database_record['formulas'] = formulas

		# 2.10 store record in database
		database.append(database_record)

	# 3. return
	return database


# function loads raw peak data from file and returns it data as array and its precision (used when processing raw peak)
def load_raw_peak(file_name):
	# 1. load raw data from file
	raw_data = genfromtxt(file_name, delimiter=',', names=True, usecols=[0, 2]) # field 'z' is not used, so skip it

	# 2. calculate total intensity
	print(raw_data)
	total_intensity = sum(raw_data['Abund'])

	# 3. create new empty array that will store 'm/z' and 'intensity' (in percentages)
	data = empty(len(raw_data), dtype=[('m/z', float64, 1), ('intensity', float64, 1)])

	# 4. fill new array
	for index in range(0, len(raw_data)):
		# 4.1 store 'm/z'
		data['m/z'][index] = raw_data['mz'][index]

		# 4.2 store 'intensity' in percentages
		data['intensity'][index] = raw_data['Abund'][index] / total_intensity * 100

	# 5. sort data by 'm/z' and revert order
	data.sort(order='m/z')
	data = data[::-1]

	# 6. search for closest pair of masses
	best_difference = data['m/z'][0] - data['m/z'][1]
	for index in range(1, len(data) - 1):
		difference = data['m/z'][index] - data['m/z'][index + 1]
		if difference < best_difference:
			best_difference = difference

	# 7. calculate precision
	precision = best_difference / 2
	#precision = 1.0079 # ################################################################################################################################################

	# 8. sort data by 'intensity' and revert order
	data.sort(order='intensity')
	data = data[::-1]

	# 9. return data and precision
	return data, precision


# load raw peak data, process it using database and save result to file
def process_raw_peak(peak_file_name, database, raw_peaks_directory, processed_peaks_directory):
	# 1. print header
	print('----------------------------------------------------------------------------------')
	print('processing peak \'' + peak_file_name + '\':')

	# 2. load peak data and show it
	data, precision = load_raw_peak(join(raw_peaks_directory, peak_file_name))
	print('peak data:')
	print(data)
	print('peak precision: ' + str(precision))

	# 3. calculate hits for each record in database
	total_hits = []
	for record in database:
		per_phenazin_hits = {'name': record['name'], 'hits': 0}

		equal_formulas = empty(len(data), dtype=[('raw mass', float64, 1), ('ethalone mass', float64, 1), ('formula', str_, 60), ('formula index', int, 1)])

		for i in range(0, len(data)):
			raw_peak_mass = data['m/z'][i]
			equal_formulas['raw mass'][i] = raw_peak_mass
			for formula_index in range(0, len(record['formulas'])):
				mass_from_database = record['formulas']['mass'][formula_index]
				if abs(raw_peak_mass - mass_from_database) < precision:
					per_phenazin_hits['hits'] = per_phenazin_hits['hits'] + 1
					equal_formulas['ethalone mass'][i] = mass_from_database
					equal_formulas['formula'][i] = record['formulas']['formula'][formula_index]
					equal_formulas['formula index'][i] = formula_index
					break
		per_phenazin_hits['equal formulas'] = equal_formulas
		total_hits.append(per_phenazin_hits)

	# 4. show
	print('hits: ')
	for hit in total_hits:
		if hit['hits'] >= 4:
			print('phenazin: ' + hit['name'])
			print('hits: ' + str(hit['hits']))
			for sub_peak_index in range(0, len(hit['equal formulas'])):
				if not hit['equal formulas'][sub_peak_index]['ethalone mass'] == 0:
					print('sub-peak index: ' + str(sub_peak_index))
					print('raw mass: ' + str(hit['equal formulas'][sub_peak_index]['raw mass']))
					print('ethalone mass: ' + str(hit['equal formulas'][sub_peak_index]['ethalone mass']))
					print('formula: ' + hit['equal formulas'][sub_peak_index]['formula'])
					print('formula index: ' + str(hit['equal formulas'][sub_peak_index]['formula index']))
					print('---')
			print('----------------------------------')

	# 4. similarity



# entry point is here

# 1. load database
database = load_database('database')
print('database loaded: ' + str(len(database)) + ' records found')

# 2. get raw peaks file names
raw_peaks_directory = 'raw/strain-B162'
processed_peaks_directory = 'processed'
raw_peak_file_names = [f for f in listdir(raw_peaks_directory) if isfile(join(raw_peaks_directory, f))]
print('==================================================================================')
print("raw peaks found: " + str(len(raw_peak_file_names)))

# 3. process all raw peaks
for peak_file_name in raw_peak_file_names:
	process_raw_peak(peak_file_name, database, raw_peaks_directory, processed_peaks_directory)