import argparse
import sys
import collections

#Page replacement algorithms

##########################################################################################

                                    #Least Recently Used

##########################################################################################

def lru(input, num_pf):
    pf_count = 0
    p_frames = collections.deque()  #list of page frames consisting of pairs (page number, last usage)
    
    #print 'input:', input
    f = open("lru_page_faults.log", "w")
    original_stderr = sys.stderr
    sys.stderr = f
    for request in input:
        #print 'Request:', request
        try:
            p_frames.remove(request)
            p_frames.appendleft(request)
        except ValueError:
            if len(p_frames) < num_pf:
                p_frames.appendleft(request)
            else:
                fault = p_frames.pop()
                p_frames.appendleft(request)
                sys.stderr.write('%s' %fault)
                sys.stderr.write('\n')
                pf_count = pf_count + 1
                    #print 'P-frames:', p_frames
    sys.stderr = original_stderr
    f.close()
    print 'Number of Page Faults:', pf_count


##########################################################################################

                                        #Second Chance

##########################################################################################

def sc(input, num_pf):
    f = open("sc_page_faults.log", "w")
    original_stderr = sys.stderr
    sys.stderr = f
    
    print 'Simulate Second Chance with', num_pf, 'page frames on', input
    
    sys.stderr = original_stderr
    f.close()


##########################################################################################

                                    #Least Frequently Used

##########################################################################################

def find_smallest(frames): #Helper function that returns INDEX of smallest count
    max_count = 0
    lru = -1
    for i in range(0, len(frames)):
        if frames[i][1] > max_count:
            max_count = frames[i][1]
            lru = i
    return lru

def incr_count (page): #Helper function to increase the count of everything in current page frames
    page[1] = page[1]+1

def lfu(input, num_pf):
    f = open("lfu_page_faults.log", "w")
    original_stderr = sys.stderr
    sys.stderr = f
    p_reqs = []
    p_frames = []  #list of page frames consisting of pairs (page number, last usage)
    
    #convert input into pairs to keep track of last usage
    for x in input:
        p_reqs.append([x, 0])
    
    for request in p_reqs:
        #print 'Request:', request
        try:
            if p_reqs[0] == 
            p_frames.remove(request)
            p_frames.appendleft(request)
        except ValueError:
            if len(p_frames) < num_pf:
                p_frames.appendleft(request)
            else:
                fault = p_frames.pop()
                p_frames.appendleft(request)
                sys.stderr.write('%s' %fault)
                sys.stderr.write('\n')
                pf_count = pf_count + 1
    #print 'P-frames:', p_frames
    sys.stderr = original_stderr
    f.close()


##########################################################################################

                                            #Random

##########################################################################################

def random(input, num_pf):
    print 'Simulate random page replacement with', num_pf, 'page frames on', input



#========================================================================================#


##########################################################################################

                                #Parsing Command Line Arguments

##########################################################################################

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




#OUTPUT: The output of your program will be every page number that was not found to be in the cache. In other words, the output of your program will be a sequence of page numbers that represents all the incoming requests that resulted in a page fault.
#you should be able to get two numbers from the unix command line (by counting the number of lines read from the input file, and the number of lines produced by your simulator).
#The first of these numbers is the total number of page/block requests your simulator program has received (you get this by counting the number of valid lines in your input file)
#he second number is how many of these page requests did result in a PAGE FAULTS (you get this by counting the number of lines produced as OUTPUT by your program - which is faithfully reproducing the page replacement algorithm's behavior).
#print out faults to stderr
#total error needs to be within 25
