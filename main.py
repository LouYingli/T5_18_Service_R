# -*- coding: utf-8 -*-
"""
@author: YingliLou
"""
import os
import csv
from shutil import copyfile, rmtree

###############################################################################
# list all the inputs which can be modify 
# define the climate zones that need to be considered
climate = ['1A','2A','2B','3A','3B','3C','4A','4B','4C','5A','5B','6A','6B','7A','8A']# define the needed climate zones

# target output (site EUI) (KBtu/ft2)
y_best_post = [47.72,49.37,48.82,52.11,48.82,41.14,58.14,52.66,49.92,65.27,58.14,74.60,66.37,82.28,119.03]
y_best_pre = [61.09,63.20,62.50,66.71,62.50,52.67,74.43,67.41,63.90,83.56,74.43,95.50,84.97,105.33,152.38]
# number of samples 
num_sample = 3
pathway = os.getcwd()

###############################################################################
# 0.change the idf file to 15 minute format
import scheduleChange as schedule
os.chdir(pathway)
## 0.1.get schedule information(15 min intervel) exclude design day schedule
schedule.schedule ('./sourceFolder_pre/1A.idf')
## 0.2.change the schedule to 15min interval    
for cz in climate:
    schedule.modify('./sourceFolder_pre/'+cz+'.idf','./results/scheduleInformation/schedule.csv',cz,'pre')
    schedule.modify('./sourceFolder_post/'+cz+'.idf','./results/scheduleInformation/schedule.csv',cz,'post')

######################################################################################
#1.sampleing: get different value of model input (LHM)

import sampleMeta as samp
os.chdir(pathway)

data_set,param_values = samp.sampleMeta(num_sample,'1A') 
with open('./results/samples/data_set.csv', 'wb') as csvfile:
    for row in data_set:
        data = csv.writer(csvfile, delimiter=',')
        data.writerow(row)   
## store the information of param_values
with open('./results/samples/param_values.csv', 'wb') as csvfile:
    for row in param_values:
        data = csv.writer(csvfile, delimiter=',')
        data.writerow(row)

###################################################################################
#2.modify IDF file and run model, get model output (site EUI)s
###model inputs and outputs are saved in './results/energy_data.csv'
import parallelSimuMeta as ps
os.chdir(pathway)
for cz in climate:
    model_results,run_time = ps.parallelSimu(cz,1,'pre')
    model_results,run_time = ps.parallelSimu(cz,1,'post')
print run_time


###################################
#choose the best operation hour
energy_data_pre=[]
with open('./results/energy_data_pre.csv', 'rb') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        energy_data_pre.append(row)

energy_data_post=[]
with open('./results/energy_data_post.csv', 'rb') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        energy_data_post.append(row)
        
err=100000
ind_best=0
#num=len(param_values) # sample number
num=6 # sample number

for i in range(1,num+1):
    temp=0
    for j in range(len(climate)):
        for k in range(len(energy_data_pre)):
            if energy_data_pre[k][0]==str(i) and energy_data_pre[k][1]==climate[j]:
                print energy_data_pre[k][0]          
                temp+=abs((float(energy_data_pre[k][-2])-y_best_pre[j])/y_best_pre[j])
        for k in range(len(energy_data_post)):
            if energy_data_post[k][0]==str(i) and energy_data_post[k][1]==climate[j]:
                print energy_data_post[k][0]          
                temp+=abs((float(energy_data_post[k][-2])-y_best_post[j])/y_best_post[j])
    temp=temp/30
    if temp < err:
        err=temp
        ind_best=i
print err
print energy_data_pre[ind_best][2]
print energy_data_post[ind_best][2]
err_avr=[]
err_avr.append(err)

with open('./results/calibration_results.csv', 'a') as csvfile:
    title_line= ['sample','climate_zone','operation hour','siteEUI','sourceEUI']
    data = csv.writer(csvfile, delimiter=',')
    data.writerow(title_line)
    for k in range(len(energy_data_pre)):
        if energy_data_pre[k][0]==str(ind_best):
            data.writerow(energy_data_pre[k])
    for k in range(len(energy_data_post)):
        if energy_data_post[k][0]==str(ind_best):
            data.writerow(energy_data_post[k])            
    data.writerow(err_avr)
  
for i in range(len(climate)):
    copyfile('./Model_pre/update_models/'+climate[i]+str(ind_best)+'.idf','./calibratedModel_pre/'+climate[i]+'.idf')
    copyfile('./Model_post/update_models/'+climate[i]+str(ind_best)+'.idf','./calibratedModel_post/'+climate[i]+'.idf')
rmtree('./Model_pre/update_models')
rmtree('./Model_post/update_models')