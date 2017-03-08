import argparse
import sys
import collections
from random import *

##########################################################################################

                                    #Least Recently Used

##########################################################################################

def lru(input, num_pf):
    pf_count = 0
    p_frames = collections.deque()
    
    f = open("lru_page_faults.log", "w")
    original_stderr = sys.stderr
    sys.stderr = f
    for request in input:
        try:
            p_frames.remove(request)
            p_frames.appendleft(request)
        except ValueError:
            if len(p_frames) < num_pf:
                p_frames.appendleft(request)
                sys.stderr.write('%s' %request)
                sys.stderr.write('\n')
                pf_count = pf_count + 1
            else:
                fault = p_frames.pop()
                p_frames.appendleft(request)
                sys.stderr.write('%s' %fault)
                sys.stderr.write('\n')
                pf_count = pf_count + 1
    sys.stderr = original_stderr
    f.close()
    print 'Number of Page Faults:', pf_count


##########################################################################################

                                    #Second Chance (Clock)

##########################################################################################

def sc(input, num_pf):
    f = open("sc_page_faults.log", "w")
    original_stderr = sys.stderr
    sys.stderr = f
    
    p_frames = []
    ref_bits = []
    pf_count = 0
    clock_hand = 0
    
    for request in input:
    	try:
    		i = p_frames.index(request) #searches for index of requested item
    		ref_bits[i] = 1 #changes reference bit of requested item to 1
    	except ValueError:
            if len(p_frames) < num_pf: #filling empty clock
                p_frames.append(request)
                ref_bits.append(1)
                sys.stderr.write('%s' %request)
                sys.stderr.write('\n')
                pf_count = pf_count + 1
            else: #search and replace
                while(1): #loop to search for page to replace    
                    if ref_bits[clock_hand] == 0: 
                        sys.stderr.write('%s' %p_frames[clock_hand])
                        sys.stderr.write('\n')
                        p_frames[clock_hand] = request 
                        ref_bits[clock_hand] = 1 
                        pf_count = pf_count + 1
                        break
                    else:
                        ref_bits[clock_hand] = 0
                    clock_hand = clock_hand + 1
                    if clock_hand >= num_pf:
                        clock_hand = 0
            clock_hand = clock_hand + 1
            if clock_hand >= num_pf:
                clock_hand = 0
    sys.stderr = original_stderr
    f.close()
    print 'Number of Page Faults:', pf_count


##########################################################################################

                                    #Least Frequently Used

##########################################################################################

def find_least(frames):
    min = frames[0]
    min_ind = 0
    for i in range(0, len(frames)):
        if frames[i] < min:
            min = frames[i]
            min_ind = i
    return min_ind

def lfu(input, num_pf):
    f = open("lfu_page_faults.log", "w")
    original_stderr = sys.stderr
    sys.stderr = f
    
    p_frames = []  #list of page frames
    p_frames_count = [] #stored as pairs [# times used, age]
    pf_count = 0

    for request in input:
        try:
            i = p_frames.index(request) #if index can be found, not a page fault
            p_frames_count[i] = p_frames_count[i]+1
            p_frames.pop(i)
            p_frames.append(request)
            move_count = p_frames_count.pop(i)
            p_frames_count.append(move_count)
        except ValueError: #page fault scenarios
            if len(p_frames) < num_pf: #fill up page table
                p_frames.append(request)
                p_frames_count.append(0)
                sys.stderr.write('%s' %request)
                sys.stderr.write('\n')
                pf_count = pf_count + 1
            else:
                fault = find_least(p_frames_count) #returns index of the least used
                sys.stderr.write('%s' %p_frames[fault])
                sys.stderr.write('\n')
                p_frames.pop(fault)
                p_frames_count.pop(fault)
                p_frames.append(request)
                p_frames_count.append(0)
                pf_count = pf_count + 1
    sys.stderr = original_stderr
    f.close()
    print 'Number of Page Faults:', pf_count


##########################################################################################

                                        #Random

##########################################################################################

def random(input, num_pf):
    f = open("random_faults.log", "w")
    original_stderr = sys.stderr
    sys.stderr = f
    
    p_frames = []
    pf_count = 0
    
    for request in input:
        try:
            p_frames.index(request)
        except ValueError:
            if len(p_frames) < num_pf:
                p_frames.append(request)
                sys.stderr.write('%s' %request)
                sys.stderr.write('\n')
                pf_count = pf_count + 1
            else:
                i = randint(0, num_pf-1)
                sys.stderr.write('%s' %p_frames[i])
                sys.stderr.write('\n')
                p_frames[i] = request 
                pf_count = pf_count + 1             
    sys.stderr = original_stderr
    f.close()
    print 'Number of Page Faults:', pf_count


#========================================================================================#
##########################################################################################

                                #Parsing Command Line Arguments

##########################################################################################
#========================================================================================#

#Parse command line arguments to select algorithm and page frame number
parser = argparse.ArgumentParser()
parser.add_argument("alg", help="Selects algorithm to simulate")
parser.add_argument("page_frame", type=int, help="Specifies the number of page frames")
args = parser.parse_args()
num_page_frames = args.page_frame

#Process input file
inf = sys.stdin
inp_list = []
page_input = 0
for line in inf:
    try:
        sentence=line.split(" ")
        for word in sentence:
            try:
                word = int(word)
                inp_list.append(word)
                page_input=page_input+1
            except ValueError:
                pass
    except ValueError:
        pass
print 'Total page requests:', page_input
if inf is not sys.stdin:
    inf.close()

#Choose algorithm
if args.alg == 'lru':
    lru(inp_list, num_page_frames)
elif args.alg == 'sc':
    sc(inp_list, num_page_frames)
elif args.alg == 'lfu':
    lfu(inp_list, num_page_frames)
elif args.alg == 'random':
    random(inp_list, num_page_frames)
else:
    print 'Must specify a valid algorithm: lru, sc, lfu, random'