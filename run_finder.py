from peak import Peak
import math


def parse_raw_line_to_components(raw_line):
    components = raw_line[:-1].replace('\t', ' ').split(' ')
    return [x for x in components if x != '']


def construct_peaks_from_input(input):
    peaks = []
    with open(input, 'r+') as f:
        index = 0
        while True:
            line = f.readline()
            if line == '':
                break

            elements = parse_raw_line_to_components(line)
            if len(elements) == 0:
                continue
            if elements[0].upper() == 'ID':
                peak = Peak()
                peak.name = elements[1]
                peak.index = index

                elements_a = parse_raw_line_to_components(f.readline())
                if elements_a[0].upper() == 'LOW':
                    for i in range(0, 10):
                        elements_low = parse_raw_line_to_components(f.readline())
                        peak.lowMass.append(float(elements_low[0]))
                        peak.lowIntensity.append(float(elements_low[1]))

                elements_a = parse_raw_line_to_components(f.readline())
                if elements_a[0].upper() == 'MID':
                    for i in range(0, 10):
                        elements_mid = parse_raw_line_to_components(f.readline())
                        peak.midMass.append(float(elements_mid[0]))
                        peak.midIntensity.append(float(elements_mid[1]))

                elements_a = parse_raw_line_to_components(f.readline())
                if elements_a[0].upper() == 'HIGH':
                    for i in range(0, 10):
                        elements_high = parse_raw_line_to_components(f.readline())
                        peak.highMass.append(float(elements_high[0]))
                        peak.highIntensity.append(float(elements_high[1]))
                index += 1
                peaks.append(peak)
    return peaks


def construct_peak_from_file(file_name):
        file = open(file_name, 'r+')
        peak = Peak()
        peak.name = file_name

        while True:
            line = file.readline()
            if line == '':
                break

            if line.upper() == 'ENERGY0\n':
                line = file.readline()
                while line.upper() != 'ENERGY1\n':
                    elements_low = parse_raw_line_to_components(line)
                    peak.lowMass.append(float(elements_low[0]))
                    peak.lowIntensity.append(float(elements_low[1]))
                    line = file.readline()

            if line.upper() == 'ENERGY1\n':
                line = file.readline()
                while line.upper() != 'ENERGY2\n':
                    elements_mid = parse_raw_line_to_components(line)
                    peak.midMass.append(float(elements_mid[0]))
                    peak.midIntensity.append(float(elements_mid[1]))
                    line = file.readline()

            if line.upper() == 'ENERGY2\n':
                line = file.readline()
                while line.upper() != '\n':
                    elements_high = parse_raw_line_to_components(line)
                    peak.highMass.append(float(elements_high[0]))
                    peak.highIntensity.append(float(elements_high[1]))
                    line = file.readline()

        return peak


def construct_peaks_from_folder(folder_name):
    database = []
    file_names = []
    for (dir_path, dir_names, additional_file_names) in walk(folder_name):
        file_names.extend(additional_file_names)

    for file_name in file_names:
        database.append(construct_peak_from_file(folder_name + '/{0}'.format(file_name)))

    return database


def comparing_input_spectra_to_database(peaks, database, error):
    distances = []
    for experiment in peaks:
        current_distances = []
        for ethalon in database:
            distance = []

            # low
            common_masses = 0
            for ethalon_mass in ethalon.lowMass:
                for experiment_mass in experiment.lowMass:
                    if abs(experiment_mass - ethalon_mass)/ethalon_mass < error:
                        common_masses += 1
                        break
            distance.append(common_masses / (len(experiment.lowMass) + len(ethalon.lowMass) - common_masses))

            # middle
            common_masses = 0
            for ethalon_mass in ethalon.midMass:
                for experiment_mass in experiment.midMass:
                    if abs(experiment_mass - ethalon_mass)/ethalon_mass < error:
                        common_masses += 1
                        break
            distance.append(common_masses / (len(experiment.midMass) + len(ethalon.midMass) - common_masses))
            
            # high
            common_masses = 0
            for ethalon_mass in ethalon.highMass:
                for experiment_mass in experiment.highMass:
                    if abs(experiment_mass - ethalon_mass)/ethalon_mass < error:
                        common_masses += 1
                        break
            distance.append(common_masses / (len(experiment.highMass) + len(ethalon.highMass) - common_masses))
            current_distances.append(distance)
        distances.append(current_distances)
    return distances


if __name__ == '__main__':
    from os import walk
    folder_name = input('Please, enter folder name with database files: ')
    input_file = input('Enter the input file name: ')
    error = float(input('Please, enter the Mass Tolerance (relative): '))

    database = construct_peaks_from_folder(folder_name)
    peaks = construct_peaks_from_input(input_file)
    distances = comparing_input_spectra_to_database(peaks, database, error)

    print(len(database))
    print(len(peaks))

    for experiment_index in range(0, len(peaks)):
        print('Peak name: {0}'.format(peaks[experiment_index].name))
        print('Similarities:')
        for ethalon_index in range(0, len(database)):
            print('{0:>115}: {1:>7.3%} + {2:>7.3%} + {3:>7.3%} = {4:>7.3%}'.format(database[ethalon_index].name,
                                                                                  distances[experiment_index][ethalon_index][0],
                                                                                  distances[experiment_index][ethalon_index][1],
                                                                                  distances[experiment_index][ethalon_index][2],
                                                                                  math.fsum(distances[experiment_index][ethalon_index])))
        print('-----------------------------------------------------------------------------------------')
