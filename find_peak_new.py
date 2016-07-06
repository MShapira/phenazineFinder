from peak import Peak
from os import walk
import math


def parse_raw_line_to_components(raw_line):
    components = raw_line[:-1].replace('\t', ' ').split(' ')
    return [x for x in components if x != '']


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


def construct_complete_data_file(input, database, error):
    new_input = []
    file = open(input, 'r+')
    for line in file:
        line_array = line.replace(',', '.').split(';')
        if line_array[0] == 'True':
            if 180 < float(line_array[6]) < 650 and float(line_array[12]) != 0:
                for compound in database:
                    # print (compound.name)
                    if abs(float(line_array[6]) - compound.lowMass[len(compound.lowMass) - 1]) <= error/1000000 * compound.lowMass[len(compound.lowMass) - 1]:
                        new_input.append(compound.name)
                        new_input.append(';')
                        new_input.append(line)
    return new_input


def make_input_clearly():
    database = construct_peaks_from_folder(input("Please enter the database name: "))
    error = float(input("Please, enter the error in ppm: "))
    new_input = construct_complete_data_file(input("Enter the file name with peaks: "), database, error)


    new_file = open('new_input.txt', 'w')
    for data in new_input:
        new_file.write(data)
    new_file.close()


make_input_clearly()