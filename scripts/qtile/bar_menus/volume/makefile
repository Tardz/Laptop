CXX = g++
CXXFLAGS = -Wall -std=c++11
GTKMM_FLAGS = $(shell pkg-config --cflags gtkmm-3.0)
GTKMM_LIBS = $(shell pkg-config --libs gtkmm-3.0)

SRC = volume_menu.cc
OBJ = volume_menu.o
TARGET = volume_menu

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) $(GTKMM_FLAGS) -o $@ $^ $(GTKMM_LIBS)

$(OBJ): $(SRC)
	$(CXX) $(CXXFLAGS) $(GTKMM_FLAGS) -c -o $@ $<

clean:
	rm -f $(OBJ) $(TARGET)