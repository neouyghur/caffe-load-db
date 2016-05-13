import numpy as np
from scipy.sparse import csr_matrix
from datetime import datetime as time
from scipy import sparse, io
from numpy import array
import os, sys, getopt

def process(input_file_name):
    crt_row_no = 0 # Current row number
    crt_col_no = 0 # Current column number
    row = []
    col = []
    data = []
    count = 0
    line = 0
    with open(input_file_name) as infile:
        for crt_line in infile:  
            value = crt_line.split(' ')
            #print value
            #result[key] = int(value)
            for v in value:
                float_v = float(v)
                #print float_v
                if float_v != 0:
                    row.append(crt_row_no)
                    col.append(crt_col_no)
                    data.append(float_v)
                    count += 1
                    if count%1000 == 0:
                        print count, line 
                #else:
                #    print 'zero'
                crt_col_no +=1
            crt_row_no += 1
            crt_col_no = 0
            line += 1
    return sparse.coo_matrix((data,(row,col))).tocsr()
    #print sp_data
    #print type(sp_data)
    #Todo:

def main(argv):
    inputfile = ''
    outputfile = ''
 
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'python <script name> -i <inputfile> -o <outputfile>'
        sys.exit(2)
 
    for opt, arg in opts:
        if opt == '-h':
            print 'python <script name> -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-o"):
            outputfile = arg
 
    print 'Reading images from "', inputfile
    print 'Writing vectors to "', outputfile

    input_file_name = inputfile

    """ ################### START PROGRAM ############################ """  

    print "--------------STRAT-----------------"
    running_time = time.now()
    data_matrix = process(input_file_name)
    print "Total time:" + str(time.now() - running_time)
    print "Writing to file."
    io.mmwrite(outputfile, data_matrix)

if __name__ == '__main__':   
    main(sys.argv[1:])