# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 12:33:30 2019

@author: Yingli Lou
"""
###############################################################
def information(file_path,schedule_name,cz):  
    print schedule_name
    f = open (file_path,'rb')
    lines = f.readlines()
    f.close()

    # get schedule of old format
    time = []
    value = []
    for i in range(len(lines)):
        if lines[i].split(',')[0].replace(' ','').lower() == 'schedule:day:interval'and lines[i+1].split(',')[0].replace(' ','') == schedule_name:
            id_time = i+4
            id_value = i+5
            for j in range(24):
                if lines[id_time].split(',')[0] == '  24:00':
                    break
                time.append(lines[id_time].split(',')[0].split(':')[0])
                value.append(lines[id_value].split(',')[0])
                id_time +=2
                id_value +=2
            time.append(lines[id_time].split(',')[0].split(':')[0])
            value.append(lines[id_value].split(';')[0])
    # generate schedule of 15-min format
    value_15min = []
    value_15min.append(schedule_name+',')
    num = 0
    num = int(time[0])
    for j in range(4*num):
        value_15min.append(value[0]+',')        
    for i in range(1,len(time)):
        num = 0
        num = int(time[i])-int(time[i-1])
        for j in range(4*num):
            value_15min.append(value[i]+',')   

    f = open ('./results/scheduleInformation/'+cz+'schedule.csv', 'ab')
    f.writelines(value_15min)
    f.writelines('\n')
    f.close()
    
#this function is designed to get schedule information(15 min intervel) exclude design day schedule
def schedule (file_path,cz):
    f = open (file_path,'rb')
    lines = f.readlines()
    f.close()
    
    schedule_name = []
    for i in range(len(lines)):
        if lines[i].split(',')[0].replace(' ','').lower() == 'schedule:day:interval'and 'DesignDay'not in lines[i+1].split(',')[0].replace(' ',''):
            schedule_name.append(lines[i+1].split(',')[0].replace(' ',''))
  
    for i in range(len(schedule_name)):
        information(file_path,schedule_name[i],cz)
########################################################################################################       
    
# This function is designed to change the schedule to 15min interval
def modify(file_path,schedule_path,cz):
    f = open (file_path,'rb')
    lines = f.readlines()
    f.close()
    
    f = open(schedule_path,'rb')
    schedule_new = f.readlines()
    f.close()
        
    # ger schedule id    
    id_start = []
    id_end = []
    
    for i in range(len(schedule_new)):
        for j in range(len(lines)):
             if lines[j].split(',')[0].replace(' ','').lower() == 'schedule:day:interval'and lines[j+1].split(',')[0].replace(' ','') == schedule_new[i].split(',')[0]:
                id_start.append(j+4)
                break_flag = 0
                for k in range(50):
                    if break_flag == 0 and lines[j+4+k].split(',')[0] == '  24:00':
                        id_end.append(j+4+k+1)
                        break_flag = 1
                    

    newlines = []
    # delete old schedule
    for i in range(len(lines)): 
        if i < int (id_start[0]):
            newlines.append(lines[i])
        if i == int (id_start[0]):
            time = 1
            newlines.append('  00:15,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
            newlines.append(schedule_new[0].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
            time += 1
            newlines.append('  00:30,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
            newlines.append(schedule_new[0].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
            time += 1
            newlines.append('  00:45,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
            newlines.append(schedule_new[0].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
            time += 1
            for k in range(1,10):
                newlines.append('  0'+str(k)+':00,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                newlines.append(schedule_new[0].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                time += 1
                newlines.append('  0'+str(k)+':15,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                newlines.append(schedule_new[0].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                time += 1
                newlines.append('  0'+str(k)+':30,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                newlines.append(schedule_new[0].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                time += 1
                newlines.append('  0'+str(k)+':45,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                newlines.append(schedule_new[0].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                time += 1
            for k in range(10,24):
                newlines.append('  '+str(k)+':00,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                newlines.append(schedule_new[0].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                time += 1
                newlines.append('  '+str(k)+':15,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                newlines.append(schedule_new[0].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                time += 1
                newlines.append('  '+str(k)+':30,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                newlines.append(schedule_new[0].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                time += 1
                newlines.append('  '+str(k)+':45,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                newlines.append(schedule_new[0].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                time += 1
            newlines.append('  24:00,                                  !- Time 96 {hh:mm}'+'\n')
            newlines.append(schedule_new[0].split(',')[96]+';                                   !- Value Until Time '+str(96)+'\n')
                
                
    for i in range(1,len(id_start)):
        for j in range(id_end[i-1],id_start[i]+1):
            if j > int(id_end[i-1]) and j < int(id_start [i]):
                newlines.append(lines[j])
            if j == int(id_start [i]):
                time = 1
                newlines.append('  00:15,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                newlines.append(schedule_new[i].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                time += 1
                newlines.append('  00:30,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                newlines.append(schedule_new[i].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                time += 1
                newlines.append('  00:45,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                newlines.append(schedule_new[i].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                time += 1
                for k in range(1,10):
                    newlines.append('  '+'0'+str(k)+':00,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                    newlines.append(schedule_new[i].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                    time +=1
                    newlines.append('  '+'0'+str(k)+':15,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                    newlines.append(schedule_new[i].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                    time +=1
                    newlines.append('  '+'0'+str(k)+':30,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                    newlines.append(schedule_new[i].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                    time +=1
                    newlines.append('  '+'0'+str(k)+':45,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                    newlines.append(schedule_new[i].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                    time +=1
                for k in range(10,24):
                    newlines.append('  '+str(k)+':00,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                    newlines.append(schedule_new[i].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                    time +=1
                    newlines.append('  '+str(k)+':15,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                    newlines.append(schedule_new[i].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                    time +=1
                    newlines.append('  '+str(k)+':30,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                    newlines.append(schedule_new[i].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                    time +=1
                    newlines.append('  '+str(k)+':45,                                  !- Time '+str(time)+' {hh:mm}'+'\n')
                    newlines.append(schedule_new[i].split(',')[time]+',                                   !- Value Until Time '+str(time)+'\n')
                    time +=1
                newlines.append('  '+str(24)+':00,                                  !- Time '+str(96)+' {hh:mm}'+'\n')
                newlines.append(schedule_new[i].split(',')[96]+';                                   !- Value Until Time '+str(96)+'\n')
                    
    for i in range(int(id_end[-1])+1,len(lines)):
        newlines.append(lines[i])
 
    f = open ('./Model/'+cz+'.idf', 'w')            
    for i in range(len(newlines)):
        f.writelines(newlines[i])
    f.close()

