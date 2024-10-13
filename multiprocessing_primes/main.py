import multiprocessing
import time
import sys
import sympy


# def child_generate_process(id, queue, start, end):
#     print("child gen", id, start, end)
#     res = []
#     for i in range(start, end):
#         if sympy.isprime(i):
#             res.append(i)
            
#     queue.put((id, res)) # return generated primes list


def child_search_process(id, arr, start, end):
    for i in range(start, end-5): # allow i to be 6 away from end on last iteration 
        n1, n2, n3 = i, i+1, i+6
        
        if n3 - n1 == 6:
            if sympy.isprime(n1) and sympy.isprime(n3):
                while sympy.isprime(n2) == False and n2 != n3:
                    n2 += 1
                if n2 != n3:
                    print("ANS", [n1, n2, n3])
                    arr[id] = [n1, n2, n3]
                    break
    
    
# class isPrime:
#     def __init__(self) -> None:
#         self.primes = []
    
#     def check(self, num):
#         b = int(math.sqrt(num)) + 1
        
#         i = 0
#         while i < len(self.primes) and (self.primes[i] < b):
#             if num % self.primes[i] == 0:
#                 return False
#             i += 1
#         return True


if __name__ == '__main__': # "python3 main.py 7" --> spawn 7 processes, default = 1
    number = input('Enter a number: ')
    number = number.replace(",", "")
    
    try:
        number = int(number)
    except:
        print("Provide a valid number!")
        sys.exit()
        
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
    # primeObj = isPrime()
    
    while end == False:
        loop += 1 
        # largestPrimeNeeded = int(math.sqrt(number + (10000 * loop)))
        # g_chunk = math.ceil(largestPrimeNeeded / nprocesses) # split up work for processes

        processes = [] 
        # nprimes = [] # current prime list
        
        # queue = multiprocessing.Queue() # create a queue for transferring generated prime lists from child processes to main
        # for i in range(nprocesses): # start all our child processes for generating prime list
        #     processes.append(multiprocessing.Process(target=child_generate_process, args=(i, queue, g_chunk*i, g_chunk*(i+1))))
        #     processes[-1].start()
        # for p in processes:
        #     p.join()
            
        # sortedLists = [[]] * nprocesses 
        # for r in range(nprocesses): # put lists in sorted order before combining all into single nprimes list
        #     curr = queue.get()
        #     id, p_sublist = curr
        #     sortedLists[id] = p_sublist
            
        # for sublist in sortedLists:
        #     nprimes += sublist
        # primeObj.primes = nprimes # save result for future iteration
        
        s_chunk = (number + (10000 * loop)) // nprocesses # split up work for processes
        manager = multiprocessing.Manager()
        shared_list = manager.list([[0, 0, 0] for _ in range(nprocesses)])
        
        print(number, number+10000, s_chunk, nprocesses, s_chunk*nprocesses)
        
        for i in range(nprocesses): 
            start, end = number + s_chunk * i, number + s_chunk * (i+1)
            if i > 1: # break search ranges up with offset of 6, edge-case: triplet is between ranges
                start -= 6
            else:
                start = number
                
            if i == nprocesses-1: # add the remaining range (fractions from the floor division) to the last chunk
                end += (number + (10000 * loop)) - (s_chunk * (i+1)) + 1
                
            processes.append(multiprocessing.Process(target=child_search_process, args=(i, shared_list, start, end,)))
            processes[-1].start()
        for p in processes:
            p.join()
            
        for lst in shared_list: # shared list has all search results in increasing order already
            if lst[0] != 0:
                ans = lst
                break
            
        if len(ans) > 0: 
            end = True
    
    print(number, ans)

