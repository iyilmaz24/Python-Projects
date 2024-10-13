import multiprocessing
import math


def child_generate_process(id, queue):
    
    queue.put((id, [5,7,11,id])) # return generated primes list
    
    print(id, "generate complete")

    
# def child_search_process(id, arr):
    
#     arr[id] = [5,7,11,id] # return first found prime triplet
#     if arr[0] > id:
#         arr[0] = id
        
#     print(id, "search complete")


if __name__ == '__main__':
    number = input('Enter a number: ')
    number = number.replace(",", "")
    number = int(number)
    
    if(number <= 5): 
        print([5, 7, 11])
    
    nprocesses = input('Number of processes: ')
    try:
        nprocesses = int(nprocesses)
    except:
        nprocesses = 4
    
    end = False
    loop = 0
    ans = [] 
    primes = []
    
    while end == False:
        loop += 1 # calculate all primes in range sqrt(loop * 10,000)
        largestPrimeNeeded = int(math.sqrt(number + (100000 * loop)))
        
        processes = [] 
        results = multiprocessing.Array("b", [1] * (nprocesses+1)) # first index will store smallest indice from successful processes when searching
        nprimes = [] # current prime list
        
        queue = multiprocessing.Queue() # create a queue for transferring generated prime lists from child processes to main
        for i in range(nprocesses): # start all our child processes for generating prime list
            processes.append(multiprocessing.Process(target=child_generate_process, args=(i+1, queue,)))
            processes[-1].start()
        for p in processes:
            p.join()
            
        if loop > 1: # if on 2nd or higher loop of primes, ex sqrt(2/3/4... * 10,000) - add last 2 primes from last iteration, edge-case: prime triplet is between ranges
            nprimes.append(primes[-2])
            nprimes.append(primes[-1])
            
        sortedLists = [] 
        for r in range(nprocesses): # put lists in sorted order before combining all into single nprimes list
            curr = queue.get()
            id, p_sublist = curr
            sortedLists[id-1] = p_sublist
            
        for sublist in sortedLists:
            nprimes += sublist
        primes = nprimes # save result for future iteration
        
        
        # for i in range(nprocesses): # break search ranges up with offset of 2, edge-case: triplet is between ranges
        #     processes.append(multiprocessing.Process(target=child_search_process, args=(i+1, results,)))
        #     processes[-1].start()
        # for p in processes:
        #     p.join()
        
        # if results[0] != 0: 
        #     ans = results[results[0]] # results[0] stores indice of earliest found prime triplet from search processes
        #     end = True
        
        end = True
             
    print(ans)

