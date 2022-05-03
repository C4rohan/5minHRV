# import necessary libraries
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import heartpy as hp
import csv 


path = os.getcwd()
# field names 
fields = ['Patient','5 Time','Day','BPM', 'ibi', 'sdnn', 'rmssd','hr_mad','sd1','sd2','sd1/sd2',] 

filename5 ="5MinMeasure.csv"
with open(filename5,'a') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)

directory = 'D:/Rohan/RA/new data/'


#numOfDirs = len(next(os.walk(directory))[1])
sub_folders = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

num = 10;
ite =1;

#print(sub_folders)
for x in sub_folders:
    ite = ite + 1

    if ite > 10 :
        break

    tempDir = directory + x + '/ECG/'
    print(tempDir);
    print ("\n")
    dir_list = os.listdir(tempDir)
    print("Files and directories in '", path, "' :")
    
   
    for singleFile in dir_list:
        
      if os.path.getsize(tempDir + singleFile)!=0:  
                    print(tempDir + singleFile + "\n")
                    data = hp.get_data(tempDir + singleFile)
                    sample_rate = 240
                    chunk_size = 72000 
                    num_chunks = len(data) // chunk_size + 1
                    #print(num_chunks)
                    first=1
                    second=chunk_size

                    if num_chunks == 1:
                        second=len(data)
                        print(num_chunks)
                    for i in range(num_chunks):
                        print(i)
                        if i >= 1:
                            first = second + 1
                            second= second + chunk_size
                            if second >= len(data):
                                second=len(data) 
                        try:
                                filtered = hp.filter_signal(data[first:second], cutoff = 0.05, sample_rate = sample_rate, filtertype='notch')
                                wd, m = hp.process(filtered, sample_rate)
                                #display computed measures
                                rows= [tempDir,i,singleFile,m['bpm'], m['ibi'], m['sdnn'], m['rmssd'],m['hr_mad'],m['sd1'],m['sd2'],m['sd1/sd2']]
                                with open(filename5 ,'a') as csvfile: 
                                # creating a csv writer object 
                                    csvwriter = csv.writer(csvfile) 
                                    # writing the data rows 
                                    csvwriter.writerow(rows)
                                    print("File _Write")
                        except:
                                print("Failed | An exception occurred")
                                try:
                                    print("Trying smoothning")
                                    smoothed = hp.smooth_signal(data[first:second], sample_rate = sample_rate, window_length=4, polyorder=2)
                                    print("Smoothed")
                                    wd, m = hp.process(smoothed, sample_rate)
                                    #display computed measures
                                    rows= [tempDir,i,singleFile,m['bpm'], m['ibi'], m['sdnn'], m['rmssd'],m['hr_mad'],m['sd1'],m['sd2'],m['sd1/sd2']]
                                    #print(rows)

                                    # writing to csv file 
                                    with open(filename5,'a') as csvfile: 
                                    # creating a csv writer object 
                                        csvwriter = csv.writer(csvfile) 
                                        csvwriter.writerow(rows)
                                    #print(rows)
                                    print("File _Written")
                                except:
                                    print("Failed at Reading")
                                    rows= [tempDir,i,singleFile,'NA','NA','NA','NA','NA','NA','NA','NA']            
                                    with open(filename5,'a') as csvfile: 
                                    # creating a csv writer object 
                                        csvwriter = csv.writer(csvfile) 
                                        csvwriter.writerow(rows)
    else:
                        print("File size 0")
                        rows= [tempDir,singleFile,'NA','NA','NA','NA','NA','NA','NA','NA']            
                        with open(filename5,'a') as csvfile: 
                    #creating a csv writer object 
                            csvwriter = csv.writer(csvfile) 
                            csvwriter.writerow(rows)
