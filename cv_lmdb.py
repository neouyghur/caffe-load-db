import lmdb
import caffe
from caffe.proto import caffe_pb2
import numpy as np

# Check dataset information before checking
def check(db_name):
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
def save2txt(db_name, outputfile):
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

# Checking part
check('features')
# Convert part
#save2txt('features', 'tempout.txt')