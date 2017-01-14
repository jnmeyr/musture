#include "network.hpp"
#include "display.hpp"

char buffer [HEIGHT];

void setup() {
  setupNetwork();
  setupDisplay();
}

void loop() {
  readNetwork(buffer);
  dimDisplay(16);
  for (unsigned int y = 0; y < HEIGHT; y++) {
    unsigned int castedValue = buffer[y];
    unsigned int scaledValue = castedValue * 8 / 255;
    unsigned int sizedValue = 2 * scaledValue - 1;
    for (int x = WIDTH / 2 - sizedValue / 2; x <= WIDTH / 2 + sizedValue / 2; x++) {
      unsigned int intensityValue = 24 * scaledValue - (int) (24 * scaledValue * abs(WIDTH / 2 - x) / ((float) (WIDTH / 2)));
      displayPoint(x, HEIGHT - y - 1, 255, intensityValue, 255);
    }
  }
  drawDisplay();
}
