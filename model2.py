
import csv
import os

skillset=['java','Java','Java EE','JAVA']
for x in range(0,20):
    file1 = os.path.normpath('validated_resumes\\resume{}.txt'.format(x))
    file2 = os.path.normpath('transformed_resumes\\transformed{}.txt'.format(x))
    with open(file1,'r') as oldfile, open(file2, 'w') as newfile:
        for line in oldfile:
            if line.startswith("Name"):
                newfile.write(line)
                    #print(line)
                    
    with open(file1,'r') as oldfile, open(file2, 'a') as newfile:
        for line in oldfile:
            #print("hello")
            if line.startswith("Skill"):
                newfile.write(line)
                #print("Skill:"+line)
                        

header = ["Name", "Skills"]
skillset=['java','Java','Java EE','JAVA']
with open('resume.csv', 'w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerow(header)

    for x in range(0,20):
        counter=0
        filepath = os.path.normpath('transformed_resumes\\transformed{}.txt'.format(x))
        with open(filepath, 'r', newline='') as f_text:
            
            #if counter==1:
                #print("hello")
            csv_text = csv.reader(f_text, delimiter=':', skipinitialspace=True)
            csv_output.writerow(row[1] for row in csv_text)
                #for line in f_text:
                 #   print(line)
   
                 
                 
                 
import pandas as pd
data = pd.read_csv('resume.csv')
data.dropna().to_csv('resume_clean.csv')                 
reader = csv.reader(open("resume_clean.csv", "r" ), delimiter=',')
f = csv.writer(open("final.csv", "w"))
for row in reader:
    
    if any(word in row[2] for word in skillset):
            f.writerow(row)
            print(row)
            
            
                    
              