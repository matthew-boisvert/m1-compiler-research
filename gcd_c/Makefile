# Source: https://www.softwaretestinghelp.com/cpp-makefile-tutorial/  
CC = /opt/homebrew/opt/llvm/bin/clang++

FLAGS = -L/opt/homebrew/opt/llvm/lib -fopenmp -O0
 
TARGET = gcd
 
all: $(TARGET) 
$(TARGET): $(TARGET).cpp
	$(CC) $(FLAGS) -o $(TARGET) $(TARGET).cpp

bc:
	$(CC) $(FLAGS) -emit-llvm -c ${TARGET}.cpp

ast:
	$(CC) $(FLAGS) -emit-ast -c ${TARGET}.cpp

clean:
	rm $(TARGET)
