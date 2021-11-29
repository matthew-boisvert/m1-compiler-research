CC = /opt/homebrew/opt/llvm/bin/clang++

FLAGS = -L/opt/homebrew/opt/llvm/lib -fopenmp -O3
 
TARGET = main
 
all: $(TARGET) 
$(TARGET): $(TARGET).cpp
	$(CC) $(FLAGS) -o $(TARGET) $(TARGET).cpp

llvm:
	$(CC) $(FLAGS) -emit-llvm -c ${TARGET}.cpp

ast:
	$(CC) $(FLAGS) -emit-ast -c ${TARGET}.cpp

clean:
	rm $(TARGET)
