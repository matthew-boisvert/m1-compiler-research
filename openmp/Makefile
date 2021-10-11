# Source: https://www.softwaretestinghelp.com/cpp-makefile-tutorial/  
CC = /opt/homebrew/opt/llvm/bin/clang++

FLAGS = -L/opt/homebrew/opt/llvm/lib -fopenmp
  
TARGET = log_threads
 
all: $(TARGET) 
$(TARGET): $(TARGET).cpp
	$(CC) $(FLAGS) -o $(TARGET) $(TARGET).cpp
clean:
	rm $(TARGET)
