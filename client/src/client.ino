#include "network.hpp"
#include "display.hpp"

char controls [4] = { 255, 255, 255, 255 };
char values [HEIGHT];

void setup() {
  setupNetwork();
  setupDisplay();
}

void loop() {
  readControls(controls);
  readValues(values);
  dimDisplay(controls[0]);
  for (unsigned int y = 0; y < HEIGHT; y++) {
    unsigned int castedValue = values[y];
    unsigned int scaledValue = castedValue * 8 / 255;
    unsigned int sizedValue = 2 * scaledValue - 1;
    for (int x = WIDTH / 2 - sizedValue / 2; x <= WIDTH / 2 + sizedValue / 2; x++) {
      unsigned int intensityValue = 24 * scaledValue - (int) (24 * scaledValue * abs(WIDTH / 2 - x) / ((float) (WIDTH / 2)));
      unsigned int red = controls[1] < 255 ? controls[1] : intensityValue;
      unsigned int green = controls[2] < 255 ? controls[2] : intensityValue;
      unsigned int blue = controls[3] < 255 ? controls[3] : intensityValue;
      displayPoint(x, HEIGHT - y - 1, red, green, blue);
    }
  }
  drawDisplay();
}
