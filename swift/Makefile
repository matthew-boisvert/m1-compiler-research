# Source: https://www.softwaretestinghelp.com/cpp-makefile-tutorial/  
CC = swiftc -Onone

FLAGS = 
  
TARGET = main
 
all: $(TARGET) 
$(TARGET): $(TARGET).swift
	$(CC) $(FLAGS) -o $(TARGET) $(TARGET).swift

bc:
	$(CC) -emit-bc ${TARGET}.swift -o ${TARGET}.bc

clean:
	rm $(TARGET)
