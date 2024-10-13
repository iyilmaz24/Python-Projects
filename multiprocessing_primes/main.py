import multiprocessing
import time
import sys
import sympy
import math


def child_search_process(id, primes, start, end):
    # print("child starting search:", id, start, "-", end)
    
    i = start
    while i < end-5: # allow i to be 6 away from end on last iteration 
        n1, n2, n3 = i, i+1, i+6
        if n3 - n1 == 6:
            if isPrime(n1, primes) and isPrime(n3, primes):
                while isPrime(n2, primes) == False and n2 != n3:
                    n2 += 1
                if n2 != n3:
                    # print("ANS", [n1, n2, n3])
                    return ([n1, n2, n3])
                i += 5
        i += 1


def child_generate_process(id, start, end):
    # print("child generating primes:", id, start, "-", end)
    res = []
    for i in range(start, end):
        if sympy.isprime(i):
            res.append(i)
            
    # print("child finished generating primes:", id, start, "-", end)
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
        largestPrimeNeeded = int(math.sqrt(number + (1000 * loop)))
        g_chunk = math.ceil(largestPrimeNeeded / nprocesses) # split up work for processes

        # processes = [0] * nprocesses 
        # queue = multiprocessing.Queue() # create a queue for transferring generated prime lists from child processes to main
        
        generateStartT = time.time()
        
        # for i in range(nprocesses): # start all our child processes for generating prime list
        #     processes[i] = (multiprocessing.Process(target=child_generate_process, args=(i, queue, g_chunk*i, g_chunk*(i+1))))
        #     processes[i].start()
        
        # sortedLists = [0] * nprocesses 
        # consumed = 0
        # while consumed < nprocesses: # put lists in sorted order before combining all into single primes list
        #     id, p_sublist = queue.get()
        #     sortedLists[id] = p_sublist
        #     consumed += 1
            
        # primes_array = []
        # # for i in range(nprocesses):
        # #     # print("joining process")
        # #     processes[i].join() 
        # for sublist in sortedLists:
        #     primes_array.extend(sublist)
            
        with multiprocessing.Pool(processes=nprocesses) as gen_pool:
            primes_array = gen_pool.starmap(
                child_generate_process,
                [(i, g_chunk*i, g_chunk*(i+1),) for i in range(nprocesses)]
            ) 
        primes_array = sum(primes_array, []) # flatten 2D array with "+" operator
        generateStopT = time.time()
        
        gen_pool.close()
        gen_pool.join()
        
        # processes = [] 
        s_chunk = (number + (1000 * loop)) // nprocesses # split up work for processes
        
        searchStartT = time.time()
        
        # for i in range(nprocesses): 
        #     start, end = number + s_chunk * i, number + s_chunk * (i+1)
        #     if i > 0: # break search ranges up with offset of 6, edge-case: triplet is between ranges
        #         start -= 6
        #     else:
        #         start = number + 1
                
        #     if i == nprocesses-1: # add the remaining range (fractions from the floor division) to the last chunk
        #         end += (number + (1000 * loop)) - (s_chunk * (i+1)) + 1
                
        #     processes.append(multiprocessing.Process(target=child_search_process, args=(i, queue, primes_array, start, end,)))
        #     processes[i].start()

        with multiprocessing.Pool(processes=nprocesses) as pool:
            results = pool.starmap(
                child_search_process,
                [(i, primes_array, 
                  number + s_chunk * i + (-6 if i > 0 else 0), 
                  number + s_chunk * (i + 1) + ((number + (1000 * loop)) - (s_chunk * (i + 1)) + 1 if i == nprocesses - 1 else number + s_chunk * (i + 1))
                 ) for i in range(nprocesses)]
            )
            

        # consumed = 0
        # minId = nprocesses
        # while consumed < nprocesses:
        #     curr = queue.get()
        #     id, q_ans = curr
        #     if id < minId and len(q_ans) > 0:
        #         minId = id
        #         ans = q_ans
        #     consumed += 1  
        # for p in processes:
        #     p.join()
        
        if len(results) > 0: 
            ans = results[0]
            stopT = time.time()
            end = True
    
    print(number, ans)
    print(f'\nTime to build the list of prime numbers: {generateStopT - generateStartT} seconds')
    print(f'Time to search for prime triplet: {stopT - searchStartT} seconds')
    print(f'Total time: {stopT - startT} seconds\n')
