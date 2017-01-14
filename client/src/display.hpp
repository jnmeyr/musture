#ifndef DISPLAY_HEADER
#define DISPLAY_HEADER

#include <FastLED.h>

const int WIDTH = 15;
const int HEIGHT = 20;
const int SIZE = WIDTH * HEIGHT;

void setupDisplay();

void clearDisplay();

void dimDisplay(int delta);

void displayPoint(int x, int y, int red, int green, int blue);

void drawDisplay();

#endif
