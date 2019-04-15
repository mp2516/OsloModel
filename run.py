import pickle
from tqdm import trange
from tqdm import tqdm
from collections import OrderedDict
from OsloModel.model import Pile
import numpy as np

if __name__ == '__main__':
    collect_all_data = False
    if collect_all_data:
        data_dict = OrderedDict()
        for length in [4, 8, 16, 32, 64, 128, 256, 512, 1024]:
            oslo_pile = Pile(length, (0.5, 0.5), (1, 2))
            pile_dict = {'heights': [], 'avalanche size': [], 'cut_off_time': 0}
            while not oslo_pile.is_steady_state:
                pile_dict['heights'].append(oslo_pile.get_pile_height())
                pile_dict['avalanche size'].append(oslo_pile.ava_size)
                oslo_pile.drop_grain()

            pile_dict['cut_off_time'] = oslo_pile.get_pile_height()
            for _ in trange(1000000):
                pile_dict['heights'].append(oslo_pile.get_pile_height())
                pile_dict['avalanche size'].append(oslo_pile.ava_size)
                oslo_pile.drop_grain()

            data_dict[length] = pile_dict
    else:
        cut_off_time = OrderedDict()
        num_sims = 10
        for length in [4, 8, 16, 32, 64, 128, 256, 512]:
            t_c = []
            print(length)
            for num in trange(num_sims):
                oslo_pile = Pile(length, (0.5, 0.5), (1, 2))
                while not oslo_pile.is_steady_state:
                    oslo_pile.drop_grain()
                t_c.append(oslo_pile.get_pile_height())
            cut_off_time[length] = [np.average(t_c), np.std(t_c)]

        pickle.dump(cut_off_time, open('cut_off_time_data', 'wb'))

