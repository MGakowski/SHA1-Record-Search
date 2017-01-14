__authors__ = ['Chick3nputer', 'Supersam654', 'MGakowski']

import hashlib
import multiprocessing
from multiprocessing import Process
from random import shuffle

chars = "0123456789abcdefefghijklmnopqrstuvwxyzQAZWSXEDCRFVTGBYHNUJMIKOLP!@#$%^&*()_+-={}[]\|;:',<.>/?`~"  # symbol add


def generate_strings(size):
    alphabet = list(chars * size)
    while True:
        shuffle(alphabet)
        for i in range(0, len(alphabet), size):
            yield ''.join(alphabet[i: i + size])


def tsum(hexhash):
    b = bytearray.fromhex(hexhash)
    return sum(b)


def nibsum(nibhash):
    b = bytearray.fromhex(nibhash)
    nsum = 0
    for byte in b:
        nsum += byte / 16
        nsum += byte % 16
    return nsum


def work():
    # Start both not at 0 and 160 to avoid a lot of startup noise.
    max_ones = 128
    min_ones = 32
    rand_length = 8 # Modify for desired rand sring length
    i = 0
    for combo in generate_strings(rand_length):
        i += 1
        if i % 100000000 == 0:
            print "Processed %d hashes." % i
        clear = combo+""  # Modify/Add something between quotes for desired entry in clear text.
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

        if hashhex[:11] == "fffffffffff":
            print "New MAX Hash Found %s:%s" % (hashhex, clear)
        elif hashhex[:11] == '00000000000':
            print "New MIN Hash Found %s:%s" % (hashhex, clear)

        tsumhex = tsum(hashhex)
        if tsumhex < 423:
            print "New Byte MIN Hash Found %s:%s:%s" % (hashhex, clear, tsumhex)
        elif tsumhex > 4728:
            print "New Byte MAX Hash Found %s:%s:%s" % (hashhex, clear, tsumhex)

        nibsumhex = nibsum(hashhex)
        if nibsumhex < 90:
            print "New Nib MIN Hash Found %s:%s:%s" % (hashhex, clear, nibsumhex)
        elif nibsumhex > 509:
            print "New Nib MAX Hash Found %s:%s:%s" % (hashhex, clear, nibsumhex)


if __name__ == '__main__':
    count = multiprocessing.cpu_count()
    for i in range(0, (count - 1)):
        p = Process(target=work)
        p.start()
        print "Starting worker %s" % (i + 1)

work()
