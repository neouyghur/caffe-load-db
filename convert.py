#!/usr/bin/env python
# Mail: osmanjan.t@gmail.com
# Date: 13 May 2016

# This program converts leveldb, lmdb dataset to txt format

import leveldb
import caffe
from caffe.proto import caffe_pb2
import numpy as np
import os, sys, getopt
import h5py

# Check dataset information before checking
def lmCheck(db_name):
    img_db = lmdb.open(db_name)
    txn = img_db.begin()
    cursor = txn.cursor()
    cursor.iternext()

    datum = caffe_pb2.Datum()
    count = 0
    for key, value in cursor:
        count = count + 1
    print 'Total features: ', count

# Convert dataset
def lmSave2txt(db_name, outputfile):
    img_db = lmdb.open(db_name)
    txn = img_db.begin()
    cursor = txn.cursor()
    cursor.iternext()

    datum = caffe_pb2.Datum()
    #count = 0
    with open(outputfile, 'w') as writer:
        writer.truncate()
        for key, value in cursor:
            datum.ParseFromString(value)
            data = caffe.io.datum_to_array(datum)
            data = np.reshape(data, (1, np.product(data.shape)))[0]
            np.savetxt(writer, data.reshape(1,-1), fmt='%.8g')
            #count = count + 1
        #print count

# Check dataset information before checking
def levCheck(db_name):
    db = leveldb.LevelDB(db_name)
    count = 0
    for key, val in db.RangeIter(): 
        count = count + 1
    print 'Total features: ', count

# Convert dataset
def levSave2txt(db_name, outputfile, file_type):
    db = leveldb.LevelDB(db_name)
    count = 0
    
    if file_type == 'text':
        with open(outputfile, 'w') as writer:
            writer.truncate()
            for key, val in db.RangeIter():
                #count = count + 1
                #print count 
                datum = caffe.io.caffe_pb2.Datum() 
                datum.ParseFromString(val) 
                data = caffe.io.datum_to_array(datum)
                np.savetxt(writer, data.reshape(1,-1), fmt='%.8g')
            #print count
    elif file_type == 'hdf5':
        with h5py.File(outputfile, 'w') as hf:
            data_matrix = []
            for key, val in db.RangeIter():
                #count = count + 1
                #print count 
                datum = caffe.io.caffe_pb2.Datum() 
                datum.ParseFromString(val) 
                data = caffe.io.datum_to_array(datum)
                data_matrix.append(data)
            data_matrix = np.array(data_matrix)
            hf.create_dataset('dataset',data=data_matrix)
            #print count
def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv,"hi:o:m:t:w:",["ifile=","ofile="])
    except getopt.GetoptError:
        print '======================================================================================='
        print 'Usage:'
        print 'convert.py -i <inputfile> -o <outputfile> -t <dataset type> -m <mode> -w <file type>'
        print 'mode -- check, convert'
        print 'dataset type -- leveldb, lmdb'
        print 'file type -- text, hdf5'
        print '======================================================================================='
        sys.exit(2)

    print "[##### Info #####]"
    for opt, arg in opts:
        if opt == '-h':
            print '======================================================================================='
            print 'Usage:'
            print 'convert.py -i <inputfile> -o <outputfile> -t <dataset type> -m <mode> -w <file type>'
            print 'mode -- check, convert'
            print 'dataset type -- leveldb, lmdb'
            print 'file type -- text, hdf5'
            print '======================================================================================='
            sys.exit()
        elif opt in ("-i"):
            inputfile = arg
            print 'Reading images from', inputfile
        elif opt in ("-o"):
            outputfile = arg
            print 'Writing vectors to', outputfile
        elif opt in ("-t"):
            dataset_type = arg
            print 'Dataset type is', dataset_type
        elif opt in ("-m"):
            mode = arg
            print 'Function mode is', mode
        elif opt in ("-w"):
            file_type = arg
            print 'Function mode is', file_type
    print '\n'

    if str.upper(dataset_type) == "LEVELDB":
        if str.upper(mode) == "CHECK": 
            levCheck(inputfile)
        elif str.upper(mode) == "CONVERT":
            levSave2txt(inputfile, outputfile, file_type)

    elif str.upper(dataset_type) == "LMDB":
        if str.upper(mode) == "CHECK":
            lmCheck(inputfile)
        if str.upper(mode) == "CONVERT":
            lmSave2txt(inputfile, outputfile)

if __name__ == '__main__':
    print '\n\n'
    print "***************** Program Start *****************"   
    main(sys.argv[1:])
