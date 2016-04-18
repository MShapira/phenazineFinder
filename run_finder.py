from peak import Peak
from numpy import genfromtxt


def parse_raw_line_to_components(raw_line):
    components = raw_line[:-1].replace('\t', ' ').split(' ')
    return [x for x in components if x != '']

#
# index = 0
# peaks = []
# with open(input('Enter the input file name: '), 'r+') as f:
#     while True:
#         line = f.readline()
#         if line == '':
#             break
#
#         elements = parse_raw_line_to_components(line)
#         if len(elements) == 0:
#             continue
#         if elements[0].upper() == 'ID':
#             peak = Peak()
#             peak.name = elements[1]
#             peak.index = index
#
#             elements_a = parse_raw_line_to_components(f.readline())
#             if elements_a[0].upper() == 'LOW':
#                 for i in range(0, 10):
#                     elements_low = parse_raw_line_to_components(f.readline())
#                     peak.lowMass.append(float(elements_low[0]))
#                     peak.lowIntensity.append(float(elements_low[1]))
#
#             elements_a = parse_raw_line_to_components(f.readline())
#             if elements_a[0].upper() == 'MID':
#                 for i in range(0, 10):
#                     elements_mid = parse_raw_line_to_components(f.readline())
#                     peak.midMass.append(float(elements_mid[0]))
#                     peak.midIntensity.append(float(elements_mid[1]))
#
#             elements_a = parse_raw_line_to_components(f.readline())
#             if elements_a[0].upper() == 'HIGH':
#                 for i in range(0, 10):
#                     elements_high = parse_raw_line_to_components(f.readline())
#                     peak.highMass.append(float(elements_high[0]))
#                     peak.highIntensity.append(float(elements_high[1]))
#             index += 1
#             peaks.append(peak)


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


if __name__ == '__main__':
    from os import walk

    file_names = []
    for (dir_path, dir_names, additional_file_names) in walk('database'):
        file_names.extend(additional_file_names)

    peaks = []
    for file_name in file_names:
        peaks.append(construct_peak_from_file('database/{0}'.format(file_name)))
        print(peaks)
