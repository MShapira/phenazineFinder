class Peak(object):
    def __init__(self):
        self.name = None
        self.index = None

        self.lowMass = []
        self.lowIntensity = []

        self.midMass = []
        self.midIntensity = []

        self.highMass = []
        self.highIntensity = []

    def __str__(self):
        return 'name: {0}\n'.format(self.name) + \
               'index: {0}\n'.format(self.index) + \
               'low mass: {0}\n'.format(self.lowMass) + \
               'low intensity: {0}\n'.format(self.lowIntensity) + \
               'mid mass: {0}\n'.format(self.midMass) + \
               'mid intensity: {0}\n'.format(self.midIntensity) + \
               'high mass: {0}\n'.format(self.highMass) + 'high intensity: {0}'.format(self.highIntensity)
