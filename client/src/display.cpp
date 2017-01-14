#include "display.hpp"

#include <FastLED.h>

#define FASTLED_ESP8266_RAW_PIN_ORDER
#define LED_SERPENTINE
#define LED_DATA_PIN 0
#define LED(x, y) leds[HEIGHT - (x & 1 ? HEIGHT - y - 1 : y) - 1 + HEIGHT * x]

CRGB leds [SIZE];

void setupDisplay() {
  FastLED.addLeds<WS2812B, LED_DATA_PIN, GRB>(leds, SIZE);
}

void clearDisplay() {
  LEDS.setBrightness(50);
  LEDS.clear();
}

void dimDisplay(int delta) {
  LEDS.setBrightness(50);
  for (int y = 0; y < HEIGHT; y++) {
    for (int x = 0; x < WIDTH; x++) {
      CRGB crgb = LED(x, y);
      LED(x, y) = CRGB(max(crgb.r - delta, 0), max(crgb.g - delta, 0), max(crgb.b - delta, 0));
    }
  }
}

void displayPoint(int x, int y, int red, int green, int blue) {
  LED(x, y) = CRGB(red, green, blue);
}

void drawDisplay() {
  LEDS.show();
}
