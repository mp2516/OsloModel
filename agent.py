from numpy.random import choice


class Site:
    def __init__(self, possible_slope, height=0):
        """

        :param possible_slope:
        :param height:
        """
        self.height = height
        self.possible_slope = possible_slope
        self.threshold_slope = choice(**possible_slope)

    def __add__(self, other):
        return self.height + other.height

    def __sub__(self, other):
        return self.height - other.height

    def reset_site(self):
        self.height = 0
        self.threshold_slope = choice(**self.possible_slope)

    def add_grain(self):
        self.height += 1

    def lose_grain(self):
        self.height -= 1
        self.threshold_slope = choice(**self.possible_slope)