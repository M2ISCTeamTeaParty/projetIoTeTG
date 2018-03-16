
class Battery(object):
    def __init__(self, id = 0, label = "", max = 0, charging_time = 0):
        self.id = id
        self.label = label
        self.etat = 0
        self.init = 0
        self.max = max
        self.charging_time = charging_time