import leveldb
import caffe
from caffe.proto import caffe_pb2
import numpy as np
import os, sys, getopt

# Check dataset information before checking
def check(db_name):
	db = leveldb.LevelDB('features')
	count = 0
	for key, val in db.RangeIter(): 
		count = count + 1
	print 'Total features: ', count

# Convert dataset
def save2txt(db_name, outputfile):
	db = leveldb.LevelDB('output/features')
	count = 0
	with open(outputfile, 'w') as writer:
		writer.truncate()
		for key, val in db.RangeIter(): 
			datum = caffe.io.caffe_pb2.Datum() 
			datum.ParseFromString(val) 
			data = caffe.io.datum_to_array(datum)
			np.savetxt(writer, data.reshape(1,-1), fmt='%.8g')
        #print count

# Checking part
#check('features')
# Convert part
#save2txt('features', 'tempout.txt')

def main(argv):
    inputfile = ''
    outputfile = ''
 
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'caffe_feature_extractor.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
 
    for opt, arg in opts:
        if opt == '-h':
            print 'caffe_feature_extractor.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-o"):
            outputfile = arg
 
    print 'Reading images from "', inputfile
    print 'Writing vectors to "', outputfile

    save2txt(inputfile, outputfile)

if __name__ == '__main__':   
    main(sys.argv[1:])