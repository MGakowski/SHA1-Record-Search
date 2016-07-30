
__authors__ = ['Chick3nputer', 'Supersam654']

from itertools import islice, product
import string
import hashlib
import multiprocessing
from multiprocessing import Process
from random import shuffle
from sys import argv

chars = "0123456789abcdefefghijklmnopqrstuvwxyzQAZWSXEDCRFVTGBYHNUJMIKOLP"

def generate_strings(size):
    alphabet = list(chars * size)
    while True:
        shuffle(alphabet)
        for i in range(0, len(alphabet), size):
            yield ''.join(alphabet[i: i + size])

def tsum(hexhash):
    return sum(int(hexhash[i: i + 2], 16) for i in range(0, len(hexhash), 2))
    
def nibsum(nibhash):
    return sum(int(nibhash[i: i + 1], 16) for i in range(0, len(nibhash), 1))
    
def work():
    # Start both not at 0 and 160 to avoid a lot of startup noise.
    max_ones = 122
    min_ones = 37
    rand_length = 12
    i = 0
    for combo in generate_strings(rand_length):
        i += 1
        if i % 100000000 == 0:
            print "Processed %d hashes." % i
        clear = combo
        hashhex = hashlib.sha1(clear).hexdigest()

        ones_count = bin(int(hashhex, 16))[2:].count('1')
        if ones_count > max_ones:
            plain = hashhex + ':' + clear
            max_ones = ones_count
            print "New Bit MAX Hash Found %s = %s" % (plain, max_ones)
        elif ones_count < min_ones:
            plain = hashhex + ':' + clear
            min_ones = ones_count
            print "New Bit MIN Hash Found %s = %s" % (plain, min_ones)

        if hashhex[:9] == "fffffffffff":
            print "New MAX Hash Found %s:%s" % (hashhex, clear)
        elif hashhex[:10] == '00000000000':
            print "New MIN Hash Found %s:%s" % (hashhex, clear)

        tsumhex = tsum(hashhex)
        if tsumhex < 598:
            print "New Byte MIN Hash Found %s:%s" % (hashhex, clear)
        elif tsumhex > 4523:
            print "New Byte MAX Hash Found %s:%s" % (hashhex, clear)
        
        nibsumhex = nibsum(hashhex)
        if nibsumhex < 116:
            print "New Nib MIN Hash Found %s:%s" % (hashhex, clear)
        elif nibsumhex > 484:
            print "New Nib MAX Hash Found %s:%s" % (hashhex, clear)

if __name__ == '__main__':
    count = multiprocessing.cpu_count()
    for i in range(0, (count - 1)):
        p = Process(target=work)
        p.start()
        print "Starting worker %s" % (i+1)
