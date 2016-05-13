#!/usr/bin/env python
# Mail: osmanjan.t@gmail.com
# Date: 13 May 2016

# This program converts leveldb, lmdb dataset to txt format

import leveldb
import caffe
from caffe.proto import caffe_pb2
import numpy as np
import os, sys, getopt

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
def levSave2txt(db_name, outputfile):
    db = leveldb.LevelDB(db_name)
    count = 0
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

def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv,"hi:o:m:t:",["ifile=","ofile="])
    except getopt.GetoptError:
        print '======================================================================================='
        print 'Usage:'
        print 'caffe_feature_extractor.py -i <inputfile> -o <outputfile> -t <dataset type> -m <mode>'
        print 'mode -- check, convert'
        print 'dataset type -- leveldb, lmdb'
        print '======================================================================================='
        sys.exit(2)

    print "[##### Info #####]"
    for opt, arg in opts:
        if opt == '-h':
            print '======================================================================================='
            print 'Usage:'
            print 'caffe_feature_extractor.py -i <inputfile> -o <outputfile> -t <dataset type> -m <mode>'
            print 'mode -- check, convert'
            print 'dataset type -- leveldb, lmdb'
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
    print '\n'

    if str.upper(dataset_type) == "LEVELDB":
        if str.upper(mode) == "CHECK": 
            levCheck(inputfile)
        elif str.upper(mode) == "CONVERT":
            levSave2txt(inputfile, outputfile)

    elif str.upper(dataset_type) == "LMDB":
        if str.upper(mode) == "CHECK":
            lmCheck(inputfile)
        if str.upper(mode) == "CONVERT":
            lmSave2txt(inputfile, outputfile)

if __name__ == '__main__':
    print '\n\n'
    print "***************** Program Start *****************"   
    main(sys.argv[1:])