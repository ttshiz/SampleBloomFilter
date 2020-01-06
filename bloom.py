# @Author Tesia Shizume

import array
import math

class BloomFilter:
    """ a simple proof of concept bloom filter """
    # This intentionally does not follow the set interface to make it distinct from sets
    # which provide guarantees not probabilistic guarantees.
    def __init__(self, filtersize, numhashes, hashfunc=hash, verbose=True):
        """ Initializes a Bloom Filter.

        Keyword arguments:
        filter_size -- array length
        numhashes -- number of hashes for each input to be entered into the filter
        hashfunc -- a hash function: expects a k wise independent hash function 
                    that takes one parameter and outputs an integer
        verbose -- enables terminal progress outputs """
        
        self.fsize = filtersize
        self.numhashes = numhashes
        self.filter = array.array('b', [0]*self.fsize)
        #TODO: more compact filter size or filter supporting delete datum
        # i.e. bitarray module, structs, or counting filter among other techniques
        self.bhash = hashfunc
        self.verbose = verbose
        #TODO: add checks for valid parameter sizes etc.

    def gen_hashes(self, datum):
        """ Takes a datum and returns a list of hashes for the datum 
        
        Using a method inspired by "Less Hashing, Same Performance: 
        Building a Better Bloom Filter" by Kirsch and Mitzenmacher """
        hashes = []
        hashes.append(datum)
        hashes.append(self.bhash(datum)) 
        for i in range(self.numhashes -1):
            hashes.append(self.bhash(str(hashes[-1])+(str(hashes[-2]))))
        hashes.remove(datum)
        return hashes 
        
    def enter_datum(self, datum):
        """ Enters a single item of data into the filter """
        hlist = self.gen_hashes(datum)
        for i in hlist:
            self.filter[i%self.fsize] = 1
        if self.verbose:
            return print("'{}' entered".format(datum))
        else:
            return

    def populate_filter(self, dataset):
        """ Enters a list of data into the filter """
        for d in dataset:
            self.enter_datum(d)
        if self.verbose:
            return print("Filter Populated")
        else:
            return
    
    def is_new_data(self, datum):
        """ Takes a datum and returns true if it is NOT found by filter """
        hlist = self.gen_hashes(datum)
        ishere = True
        for h in hlist:
            ishere = ishere and (self.filter[h%self.fsize] == False)
        return ishere

    def prob_fp(self, datasetsize):
        """ Calculates the probability of a false positive using the Bloom Filter 
        Parameters and the datasetsize 

        References: 
        -Probability and computing: Randomized algorithms and probabilistic analysis 
          by Mitzenmacher and Upfal(2005)
        -https://web.archive.org/web/20191220071455/https://en.wikipedia.org/wiki
         /Bloom_filter#Probability_of_false_positives"""
        return (1 - math.exp(-(self.numhashes*datasetsize)/self
                             .fsize))**self.numhashes
                
    def __str__(self):
        return str(self.filter)

# General TODOs:
### Align scoping with standards of hypothetical greater project
### Consider the merits of eliminating or changing default parameters in context of users
### Enforce use of k wise independent hash function
### Extend test classes

def print_result(test_string, bfilter):
    print("-Testing if '{}' is new data... {}"
          .format(test_string, str(bfilter.is_new_data(test_string))))
    return

def main():
    # instantiate filter
    aFilter = BloomFilter(2**20, 5, hashfunc=hash, verbose=False)
    
    # demonstrate single entry
    print("---Single Entry Example---")
    print("Empty Filter Query")
    print_result("8", aFilter)
    
    print("Single Entry: '8'")
    aFilter.enter_datum("8")
    
    print("Filter Queries:")
    print_result("Hi", aFilter)
    print_result("8", aFilter)
    print_result("Hellow World", aFilter)
   
    # demonstrate dataset entry
    print("\n---Dataset Entry Example---")
    with open("words.txt") as fp:
        words = [i.strip() for i in fp]
    aFilter.populate_filter(words)

    print("Filter Queries:")
    print_result("Hi", aFilter)
    print_result("8", aFilter)
    print_result("Hello World", aFilter)
    print_result("Artic", aFilter)
    print_result("arctic", aFilter)
    print_result("Arctic", aFilter)
    print_result("zillions", aFilter)
    print_result("xdxdx", aFilter)
    print_result("asdfg", aFilter)
    print_result("zzzzzz", aFilter)
    print_result("cdfghjk", aFilter)

if __name__ == '__main__':
    main()
