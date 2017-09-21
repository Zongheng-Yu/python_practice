class creature(object):
    WHO_AM_I = 'creature'

    def __init__(self):
        self.name = 'creature'

    def self_introduction(self):
        print self.WHO_AM_I + ' is '+ self.name


class animal(creature):
    WHO_AM_I = 'animal'

    def __init__(self):
        super(animal, self).__init__()
        self.name = 'animal'
        pass

class plant(creature):
    def __init__(self):
        super(plant, self).__init__()
        self.name = 'plant'
        pass


class Microorganism(creature):
    WHO_AM_I = 'microorganism'

    def __init__(self):
        self.name = 'microorganism'
        pass

    def self_introduction(self):
        print "Hello, ",
        super(Microorganism, self).self_introduction()


if __name__ == '__main__':
    animal().self_introduction()
    plant().self_introduction()
    Microorganism().self_introduction()