all: GetPulsesFromTime GetPulsesFromTimeOptimized GetRandomPulses GetPulsesFromRun
CC = g++
CFLAGS= -g -Wall `diana-config --cflags`
LDFLAGS = `diana-config --libs`

GetPulsesFromTime: GetPulsesFromTime.cpp 
	$(CC) GetPulsesFromTime.cpp $(CFLAGS) $(LDFLAGS) -o GetPulsesFromTime

GetPulsesFromTimeOptimized: GetPulsesFromTimeOptimized.cpp 
	$(CC) GetPulsesFromTimeOptimized.cpp $(CFLAGS) $(LDFLAGS) -o GetPulsesFromTimeOptimized

GetRandomPulses: GetRandomPulses.cpp
	$(CC) GetRandomPulses.cpp $(CFLAGS) $(LDFLAGS) -o GetRandomPulses

GetPulsesFromRun: GetPulsesFromRun.cpp
	$(CC) GetPulsesFromRun.cpp $(CFLAGS) $(LDFLAGS) -o GetPulsesFromRun

clean:
	rm ./GetPulsesFromTime ./GetPulsesFromTimeOptimized ./GetRandomPulses ./GetPulsesFromRun
