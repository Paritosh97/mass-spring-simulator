all:
	g++ -c src/*.cpp
	g++ *.o -lm -lglut -lGLU -lGL -o fast-cloth-sim