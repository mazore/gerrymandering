from constants import NUM_PROCESSES
from multiprocessing import Pool
from root import Root


if __name__ == '__main__':
    if NUM_PROCESSES == 1:
        Root()
    else:
        with Pool(NUM_PROCESSES) as pool:
            pool.map(Root.__call__, range(NUM_PROCESSES))
