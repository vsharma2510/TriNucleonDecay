#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 18:44:09 2022

Script to get list of run numbers and times of high multiplicity events from json file

@author: Vivek Sharma
"""

import json, datetime

#Opening json file
filepath = '/global/projecta/projectdirs/cuore/scratch/vsharma/Tri_proton_decay/High_multiplicity_events_study/GroupedEventsAndTimesM10Count10.json'
filetext = open(filepath, 'r').read()
object = json.loads(filetext)

with open("EventTimesAndRunNumbers.txt",'w') as output:
    for event in object:
        #Getting run number, first channel, datetime object from json file
        runNumber = event['RunNumber']
        eventDatetime = datetime.datetime.fromisoformat(event['GroupedEventDatetime'])
        channel = event['CrystalNumbers'][0]
        runStartDatetime = datetime.datetime.fromisoformat(event['RunNumberStartDatetime'])
        timeDifference = event['Time']
        output.write(str(runNumber) + ',' + str(channel) + ',' + str(timeDifference) + '\n')
    
