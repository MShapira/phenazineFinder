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
    for peak in peaks:
        for i in range(len(peak.lowMass)):
            for entity in database:
                for j in range(len(entity.lowMass)):
                    if float(abs(peak.lowMass[i] - entity.lowMass[j])) <= error:
                        distance = math.sqrt((peak.lowMass[i] - entity.lowMass[j])**2 +
                ((peak.lowIntensity[i]/math.fsum(peak.lowIntensity)*100) - entity.lowIntensity[j])**2)
                        entity.lowDistances.append(distance)
        for i in range(len(peak.midMass)):
            for entity in database:
                for j in range(len(entity.midMass)):
                    if abs(peak.midMass[i] - entity.midMass[j]) <= error:
                        distance = math.sqrt((peak.midMass[i] - entity.midMass[j])**2 +
                                ((peak.midIntensity[i]/math.fsum(peak.midIntensity)*100) - entity.midIntensity[j])**2)
                        entity.midDistances.append(distance)
        for i in range(len(peak.highMass)):
            for entity in database:
                for j in range(len(entity.highMass)):
                    if abs(peak.highMass[i] - entity.highMass[j]) <= error:
                        distance = math.sqrt((peak.highMass[i] - entity.highMass[j])**2 +
                                ((peak.highIntensity[i]/math.fsum(peak.highIntensity)*100) - entity.highIntensity[j])**2)
                        entity.highDistances.append(distance)

if __name__ == '__main__':
    from os import walk
    folder_name = input('Please, enter folder name with database files: ')
    input_file = input('Enter the input file name: ')
    error = float(input('Please, enter the Mass Tolerance in Da: '))

    database = construct_peaks_from_folder(folder_name)
    peaks = construct_peaks_from_input(input_file)
    comparing_input_spectra_to_database(peaks, database, error)

    print(len(database))
    print(len(peaks))
