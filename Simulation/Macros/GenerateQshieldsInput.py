import random
import time

numberOfBatches = 100 #Number of output files
numberOfEntries = 250 #Number of lines in each file

#Looping over output files
for i in range(numberOfBatches):
    #Name of each file !!! CHANGE FOR DIFFERENT BATCH SIZE OR ENTRY NUMBERS
    filename = "/home/vivek9/TriProtonDecay/Simulation/Input/QShieldsInputs/ppp25k/QshieldsInputBatch" + str(i) + ".txt"
    #Opening file
    with open(filename, 'w') as file:
        #Generating energies for each line
        for j in range(numberOfEntries):
            random.seed()
            x = random.random()
            y = random.random()
            #If random numbers generated are equal, generate again
            while x==y:
                random.seed()
                x = random.random()
                y = random.random()
            #If any of the numbers are zero, generate again
            while (x==0 or y==0):
                random.seed()
                x = random.random()
                y = random.random()
            #If x is greater than y, swap their values
            if x>y:
                temp = x
                x = y
                y = temp
            #Calculate partitions from x and y
            a = x
            b = y - x
            c = 1 - y

            if(j<numberOfEntries-1):
                file.write(str(3) + ' ' +  'pi+' + ' ' + str(a*2710) + ' ' + str(0) + ' ' + 
                                    'pi+' + ' ' + str(b*2710) + ' ' + str(0) + ' ' + 
                                    'p' + ' ' + str(c*2710) + ' ' + str(0) + '\n')

            #For last line, do not include a newline
            if(j==numberOfEntries-1):
                file.write(str(3) + ' ' +  'pi+' + ' ' + str(a*2710) + ' ' + str(0) + ' ' + 
                                    'pi+' + ' ' + str(b*2710) + ' ' + str(0) + ' ' + 
                                    'p' + ' ' + str(c*2710) + ' ' + str(0))
        
            #print('a: ' + str(a))
            #print('b: ' + str(b))
            #print('c: ' + str(c))
            #print('Total: ' + str(a+j+k))
            #print('----------------------------')
