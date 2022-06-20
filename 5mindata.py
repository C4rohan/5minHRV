# import necessary libraries
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import heartpy as hp
import csv 
import BinarySearch

path = os.getcwd()
# field names 
fields = ['Patient','5Min Time','Start time','End Time','Day','Coverage','BPM', 'ibi', 'sdnn', 'rmssd','hr_mad','sd1','sd2','sd1/sd2',] 

filename5 ="5MinMeasure.csv"
with open(filename5,'a') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)

directory = 'D:/Rohan/RA/waveform/'


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
            print(tempDir + singleFile + " --end\n")

            #samplefile = 'D:\Rohan\RA\waveform\p2_Patient\ECG\ECG_1.csv'
            timedata = hp.get_data(tempDir + singleFile, column_name = 'Time2')
            data = hp.get_data(tempDir + singleFile, column_name = 'Value')
            
            print("Test")
            sample_rate = 240
            chunk_size = 72000 
            num_chunks = len(data) // chunk_size + 1
            #print(num_chunks)
            first=1
            second=chunk_size

            if num_chunks == 1:
                second=len(data)
                print(num_chunks)

            for i in range(num_chunks * 1000):
                print(i)
                if i >= 1:
                    first = second + 1
                    second= second + chunk_size
                    if second >= len(data):
                        second=len(data)
                    try:
                        if timedata[second] - timedata[first] < 300:
                            second = second + 240
                    except:
                        print()
                    az=(timedata[first:second])
                    temp_az = np.rint(az)
                    az_unique = np.unique(temp_az)
                    
                    if len(az_unique) == 0:
                        break

                    first_val = az_unique[0]
                    for j in range(1,len(az_unique)):
                        #print('val i ' +str(az_unique[i]) + 'val i-1 '+str(az_unique[i-1]))
                        if(az_unique[j] - az_unique[j-1] > 10):
                            #second = ((i-1) * 240) + first


                            # Function call
                            result = BinarySearch.binary_search(temp_az, 0, len(temp_az)-1, az_unique[j-1])
                            if result != -1:
                                print("Element is present at index", str(result))
                                second = first + result
                                print("Actual value " + str(timedata[second-1]) + " " + str(timedata[second]) + " " + str(timedata[second+1]))
                            else:
                                print("Element is not present in array | element--> " + str(az_unique[j-1]))
                            break

                    
                    print("first -- " + str(first))
                    print("second -- " + str(second))
                try:
                        filtered = hp.filter_signal(data[first:second], cutoff = 0.05, sample_rate = sample_rate, filtertype='notch')
                        per= round((len(filtered)/chunk_size)*100, 2)
                        wd, m = hp.process(filtered, sample_rate)
                        #m=timedata[first]
        
                        F=timedata[first]
                        S=timedata[second]

                        print("timedata",F)
                        print("timedata",S)

                        #display computed measures
                        rows= [tempDir,i,F,S,singleFile,per,m['bpm'], m['ibi'], m['sdnn'], m['rmssd'],m['hr_mad'],m['sd1'],m['sd2'],m['sd1/sd2']]
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
                            per1= (len(smoothed)/len(timedata))*100
                            wd, m = hp.process(smoothed, sample_rate)
                            F=timedata[first]
                            S=timedata[second]
                            #display computed measures
                            rows= [tempDir,i,F,S,singleFile,per1,m['bpm'], m['ibi'], m['sdnn'], m['rmssd'],m['hr_mad'],m['sd1'],m['sd2'],m['sd1/sd2']]
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
                            per1=(len(data[first:second])/chunk_size)
                            rows= [tempDir,i,'NA','NA',singleFile,per1,'NA','NA','NA','NA','NA','NA','NA','NA']            
                            with open(filename5,'a') as csvfile: 
                            # creating a csv writer object 
                                csvwriter = csv.writer(csvfile) 
                                csvwriter.writerow(rows)
      else:
            print("File size 0")
            rows= [tempDir,i,'NA','NA',singleFile,'NA','NA','NA','NA','NA','NA','NA','NA','NA']            
            with open(filename5,'a') as csvfile: 
        #creating a csv writer object 
                csvwriter = csv.writer(csvfile) 
                csvwriter.writerow(rows)
