from peak import Peak
from numpy import genfromtxt


def parse_raw_line_to_components(raw_line):
    components = raw_line[:-1].replace('\t', ' ').split(' ')
    return [x for x in components if x != '']


index = 0
peaks = []
with open(input('Enter the input file name: '), 'r+') as f:
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


def construct_substances_for_database(file_name):
        file_data = genfromtxt(file_name, dtype=None, delimiter=' ', names=True)
        peak = Peak()
        peak.name = file_name

        for line in file_data:
            if len(line) == 0:
                continue
            if line[0].upper() == 'ENERGY0':
                while line[0].upper() != 'ENERGY1':
                    elements_low = parse_raw_line_to_components(file_name.readline())
                    peak.lowMass.append(float(elements_low[0]))
                    peak.lowIntensity.append(float(elements_low[1]))

            if line[0].upper() == 'ENERGY1':
                while line[0].upper() != 'ENERGY2':
                    elements_mid = parse_raw_line_to_components(file_name.readline())
                    peak.midMass.append(float(elements_mid[0]))
                    peak.midIntensity.append(float(elements_mid[1]))

            if line[0].upper() == 'ENERGY2':
                while line[0].upper() != '':
                    elements_high = parse_raw_line_to_components(file_name.readline())
                    peak.highMass.append(float(elements_high[0]))
                    peak.highIntensity.append(float(elements_high[1]))

        return peak

# print('peaks loaded: {0}'.format(index))
# print()
# for peak in peaks:
#     print(peak)
#     print()
