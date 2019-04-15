import numpy as np
from .agent import Site

class Pile:
    def __init__(self, length, slope_probabilities, threshold_slope):
        """
        Each Pile contains an array of sites, called a 'lattice'.
        :param length:
        :param slope_probabilities:
        :param threshold_slope:
        """
        possible_slope = dict(a=threshold_slope, p=slope_probabilities)
        self.length = length
        # each site will be generated with a unique threshold slope as Site() is given the probabilities
        self.lattice = np.array([Site(possible_slope) for _ in range(self.length)])
        self.avalanche_size = 0
        self.is_steady_state = False

    def get_pile_height(self):
        """Returns the height of 0th site, which is defined as the oslo_pile height"""
        return self.lattice[0].height

    def get_heights(self):
        """Returns the height of all sites"""
        return list([site.height for site in self.lattice])

    def get_threshold_slopes(self):
        """Returns the threshold slope of all sites"""
        return list([site.threshold_slope for site in self.lattice])

    def reset_pile(self):
        """Resets all sites in the lattice and returns them to the steady state"""
        for site in self.lattice:
            site.reset_site()
        self.is_steady_state = False

    def get_unstable_site_indices(self):
        """
        Returns a list of indices of the unstable sites.
        all_slopes: produces a list of all the slopes in the lattice. The list has the same length as the length
        of the lattice and the first element is the difference in slope between the first and second site and the
        last element is the height of the last site (which is the slope between it and the end of the lattice).
        """
        all_slopes = np.append(self.lattice[:-1] - self.lattice[1:],
                               self.lattice[-1].height)
        return [site_index for site_index, site in enumerate(self.lattice)
                if all_slopes[site_index] > site.threshold_slope]

    def drop_grain(self, site_index=0):
        """
        Add a grain to a specific site (0 in the Oslo Model). Causes the unstable sites to relax and counts the
        avalanche size.
        :param site_index: This is 0 in the Oslo Model and any index between 0 and self.length in the BTW Model
        :return: None
        """
        # reset avalanche size counter
        self.avalanche_size = 0

        # drive
        self.lattice[site_index].add_grain()

        while True:
            # find sites that need relaxing
            unstable_site_indices = self.get_unstable_site_indices()
            if not unstable_site_indices:
                # there are no unstable sites so stop iterating the avalanche
                break

            # relax unstable sites
            for unstable_site_index in unstable_site_indices:
                self.relax(unstable_site_index)

    def relax(self, unstable_site_index):
        """
        Relax the unstable site and count the avalanche size. If the unstable site is the last site then allow
        the grain to leave the system.
        :param unstable_site_index: The index of the unstable site
        :return: None
        """
        # z_i -> z_i - 1
        self.lattice[unstable_site_index].lose_grain()
        self.avalanche_size += 1

        # allow the grain to leave the system at the last site
        if unstable_site_index == self.length - 1:
            self.is_steady_state = True
        else:
            # z_{i+1} -> z_{i+1} + 1
            self.lattice[unstable_site_index + 1].add_grain()

