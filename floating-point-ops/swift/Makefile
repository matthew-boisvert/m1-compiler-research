CC = swiftc

FLAGS = -O
  
TARGET = main
 
all: $(TARGET) 
$(TARGET): $(TARGET).swift
	$(CC) $(FLAGS) -o $(TARGET) $(TARGET).swift

llvm:
	$(CC) -emit-ir ${TARGET}.swift -o ${TARGET}.ll

clean:
	rm $(TARGET)
