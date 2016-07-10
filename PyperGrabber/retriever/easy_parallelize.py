from multiprocessing import Pool
# from multiprocessing.dummy import Pool # use this module for threading: default is processing


"""
NOTE: WORKS only when only a single argument/parameter needs to be passed to worker func!

http://chriskiehl.com/article/parallelism-in-one-line/
https://www.binpress.com/tutorial/simple-python-parallelism/121

speed of multithreading vs. multiprocessing:
http://eli.thegreenplace.net/2012/01/16/python-parallelizing-cpu-bound-tasks-with-multiprocessing/

multiple arguments:
https://stackoverflow.com/questions/5442910/python-multiprocessing-pool-map-for-multiple-arguments
"""


def easy_parallelize(func, data, pool_size=None):
    if pool_size is None or pool_size < 1:  # make number of workers fit size of input data, if not specified otherwise
        pool = Pool(processes=len(data))
    else:
        pool = Pool(processes=pool_size)

    results = pool.map(func, data)

    cleaned = filter(None, results)  # cleaning out None results

    pool.close()
    pool.join()

    return cleaned


