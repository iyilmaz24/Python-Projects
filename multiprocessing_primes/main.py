import multiprocessing
import time
import sys
import sympy
import math


def child_prime_check(i, primes, task_queue, result_queue):
    while True:
        i = task_queue.get()
        if i == -1:
            break
        
        if isPrime(i, primes):
            result_queue.put(i)
        task_queue.task_done()


def child_generate_process(start, end):
    res = []
    for i in range(start, end):
        if sympy.isprime(i):
            res.append(i)
            
    return res # return generated primes list


def isPrime(num, primes):
    b = int(math.sqrt(num)) + 1
    i = 0
    while i < len(primes) and (primes[i] < b):
        if num % primes[i] == 0:
            return False
        i += 1
    return True

    
if __name__ == '__main__': # "python3 main.py 7" --> spawn 7 processes, default = 1

    number = input('Enter a number: ')
    number = number.replace(",", "")
    try:
        number = int(number)
    except:
        print("Provide a valid number!")
        sys.exit()
        
    startT = time.time()
        
    if(number <= 5): 
        print([5, 7, 11])
        sys.exit()
    
    if (len(sys.argv) > 1):
        nprocesses = int(sys.argv[1])
    else:
        nprocesses = 1
    
    end = False
    loop = 0
    ans = [] 
    
    while end == False:
        loop += 1 
        largestPrimeNeeded = int(math.sqrt(number + (10000 * loop)))
        g_chunk = math.ceil(largestPrimeNeeded / nprocesses) # split up work for processes

        generateStartT = time.time()
            
        with multiprocessing.Pool(processes=nprocesses) as gen_pool:
            primes_array = gen_pool.starmap(
                child_generate_process,
                [(g_chunk*i, g_chunk*(i+1),) for i in range(nprocesses)]
            ) 
        primes_array = sum(primes_array, []) # flatten 2D array with "+" operator
        gen_pool.close()
        gen_pool.join()
        generateStopT = time.time()
        
        searchStartT = time.time()
        result_queue = multiprocessing.Queue()
        task_queue = multiprocessing.JoinableQueue()
        
        processes = [] 
        s_chunk = (number + (10000 * loop)) // nprocesses # split up work for processes
        for i in range(nprocesses):
            processes.append(multiprocessing.Process(target=child_prime_check, args=(i, primes_array, task_queue, result_queue)))
            processes[i].start()
        
        j = 0
        primes_range_sorted = []
        while j < (number+10000 // 100) + 1 and end == False: # max range of 10,000 past number, increments of 100
            
            for i in range(number+(j*100), number+((1+j)*100)):
                task_queue.put(i)
                
            task_queue.join()
            
            primes_range = []
            while not result_queue.empty():
                primes_range.append(result_queue.get())
                
            primes_range.sort()
            if len(primes_range_sorted) > 0:
                primes_range_sorted = [primes_range_sorted[-2], primes_range_sorted[-1]]
            primes_range_sorted.extend(primes_range)
            
            for i in range(2, len(primes_range_sorted)):
                n1, n2, n3 = primes_range_sorted[i-2], primes_range_sorted[i-1], primes_range_sorted[i]
                if n3 - n1 == 6:
                    ans = [n1, n2, n3]
                    end = True
                    break
                
            j += 1 # check next range of 100 numbers for prime triplet
            
        for i in range(nprocesses): # terminate processes
            task_queue.put(-1)
            
        if len(ans) > 0: 
            stopT = time.time()
            end = True
        
    # print(number, ans)
    print(f'\nTime to build the list of prime numbers: {generateStopT - generateStartT} seconds')
    print(f'Time to search for prime triplet: {stopT - searchStartT} seconds')
    print(f'Total time: {stopT - startT} seconds\n')
