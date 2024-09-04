
import sympy

number = input('Enter a number: ')
number = number.replace(",", "")
number = int(number)

def findSmallestPrime(num):
    trplt = None
    if(num <= 5): 
        return [5, 7, 11] 
    
    curr = num
    end = False
    
    while(curr < num or end == False):
        if(trplt != None and num <= trplt[0]):
            end = True
        

        if (sympy.isprime(curr)):
            if (sympy.isprime(curr + 6)):
                innerNum = curr + 1
                while(sympy.isprime(innerNum) == False and innerNum < curr + 6):
                    innerNum += 1
                if(innerNum != curr + 6):
                    trplt = [curr, innerNum, curr + 6]
                    # print(trplt)

        curr += 1        
    
    return trplt



triplet = findSmallestPrime(number)
print(f"The smallest triplet larger than {number} is ({triplet[0]}, {triplet[1]}, {triplet[2]})")