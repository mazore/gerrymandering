from multiprocessing import Pool
from parameters import NUM_PROCESSES
from root import Root


if __name__ == '__main__':
    if NUM_PROCESSES == 1:
        Root()
    else:  # if multiple windows
        with Pool(NUM_PROCESSES) as pool:
            pool.map(Root.__call__, range(NUM_PROCESSES))
