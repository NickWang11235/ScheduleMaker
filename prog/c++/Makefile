CXX=g++

CXXFLAGS=-std=c++11

timeframe: timeframe.o
	${CXX} ${CXXFLAGS} timeframe.o -o timeframe

utility: utility.o pugixml.o
	${CXX} ${CXXFLAGS} utility.o pugixml.o -o utility

timeframe.o: timeframe.cpp
	${CXX} ${CXXFLAGS} -c timeframe.cpp

clean:
	del -f *.o *.exe
