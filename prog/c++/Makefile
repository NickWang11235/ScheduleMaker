CXX=g++

CXXFLAGS=-std=c++11

timeframe: timeframe.o
	${CXX} ${CXXFLAGS} timeframe.o -o timeframe

timeframe.o: timeframe.cpp
	${CXX} ${CXXFLAGS} -c timeframe.cpp

clean:
	del -f *.o *.exe
