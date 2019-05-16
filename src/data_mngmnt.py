import os
import cv2
import boto3
import numpy as np
import sys
import tlsh
import psycopg2

if not os.path.exists("config.py"):
    os.system("chmod +x configen.sh")
    os.system("./configen.sh")

import config as c

class DataObject:
    '''
    Class to represent a keypoint to write to database

    self.pt: (Float, Float)
    self.size: Float
    self.angle: Float
    self.octave: Int
    self.class_id: Int
    self.desc: Numpy Array

    '''
    def __init__(self, pt, size, angle, response, octave, class_id, desc):
        '''
        Initalises variables for function
        '''
        self.pt = pt
        self.size = size
        self.angle = angle
        self.response = response
        self.octave = octave
        self.class_id = class_id
        self.desc = desc

    def __str__(self):
        '''
        Returns string representation for output to database
        '''
        return f'{self.pt}|{self.size}|{self.angle}|{self.response}|\
                {self.octave}|{self.class_id}|{self.desc}'

def pack_keypoints(keypoints, desc):
    '''
    This will take a list of opencv keypoints and turn them into a list of 
    DataObjects definined above

    keypoints: List
    desc: Numpy Array

    Returns: List (of DataObjects)
    '''
    kp_lst = []
    i = 0
    for point in keypoints:
        tmp_desc = np.array_str(desc[i]).replace('\n','')
        tmp = DataObject(point.pt, point.size, point.angle, point.response, \
                            point.octave, point.class_id, tmp_desc)
        i += 1
        kp_lst.append(tmp.__str__())
    return kp_lst

def unpack_keypoints(kp_lst):
    '''
    Take list of DataObjects and converts back to list of opencv keypoints

    Returns: (List, Numpy Array)
    '''
    kp = []
    desc = []
    kp_lst = kp_lst.split('\n')
    for item in kp_lst:
        item = item.split('|')
        tmp_x,tmp_y = eval(item[0])
        kp.append(cv2.KeyPoint(x=tmp_x,y=tmp_y,_size=float(item[1]),
                              _angle=float(item[2]),_response=float(item[3]), 
                              _octave=int(item[4]),_class_id=int(item[5])))
        tmp_desc = ' '.join(item[6:])[1:-1]
        #print(np.fromstring(tmp_desc, sep='.'))
        tmp_str = ''
        for char in tmp_desc:
            if char == '.':
                tmp_str += char + ' '
            else:
                tmp_str += char
        desc.append(np.fromstring(tmp_str, sep=' '))
    return kp, np.array(desc) 

def connect_postgres():
    '''
    Opens a connection to a postgres database

    Returns: Database connection object
    '''
    conn_str = f"dbname='{c.dbname}' user='{c.user}' \
            host='{c.host}' port={c.port} password='{c.password}'"
    try:
        conn = psycopg2.connect(conn_str)
        f = open('panic.log', 'w')
        f.write('Connection success\n')
        f.close()
    except psycopg2.Error as e:
        f = open('panic.log', 'w')
        f.write('Connection not success')
        f.close()
        return ("Database connection error: ", e)
    return conn

def sanatise(string):
    string = '\n'.join(string)
    out_string = ''
    for char in string:
        #if char == "'":
        #    out_string += "\""
        if char == ' ': 
            pass
        else:
            out_string += char
    return out_string

def write_postgres(dhash, datapoint, url='Unknown'):
    '''
    Takes a hash of datapoint, datapoint and source url and writes that to the database

    dhash: String (Hash of datapoints)
    datapoint: String (Keypoints of an image)
    url: String (Source of image)

    Returns None
    '''
    conn = connect_postgres()
    cur = conn.cursor()
    datapoint = sanatise(datapoint)
    string = f"INSERT INTO curartdata VALUES ('{str(dhash)}', '{url}', '{str(datapoint)}');"
    cur.execute(string)
    conn.commit()
    conn.close()
    return

def query_postgres(dhash):
    '''
    Reads in a hash and queries database for a similar hash

    dhash: String (Hash of keypoints)

    Returns: String (Results of query)
    '''
    conn = connect_postgres()
    print(type(conn))
    cur = conn.cursor()
    # levenshtein was 13
    cur.execute(f"SELECT hash, url, datapoint \
                  FROM curartdata \
                  WHERE levenshtein(hash, \'{dhash}\') <= 39 \
                  ORDER BY levenshtein(hash, \'{dhash}\') \
                  LIMIT 5;")
    #cur.execute(f"SELECT hash, url, datapoint FROM curartdata;")
    results = cur.fetchall()
    conn.close()
    return  results

if __name__ == '__main__':
    org_img = cv2.imread('orginal.jpg')
    kp,desc = get_keypoints(org_img)

    if len(sys.argv) > 1 and sys.argv[1] == '-g':
        org_results = cv2.drawKeypoints(org_img, kp, None, color=(0, 255, 0))
        cmp_results = cv2.drawKeypoints(org_img, kp_2, None, color=(0, 255, 0))
        cv2.imshow("Org", org_results)
        cv2.imshow("Cmp", cmp_results)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
