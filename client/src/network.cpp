#include "network.hpp"

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "display.hpp"

WiFiUDP udp;
unsigned int lastCount = 0;

void setupNetwork() {
  WiFi.mode(WIFI_STA);
  WiFi.begin("", "");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }

  udp.begin(50001);
}

void readNetwork(char * buffer) {
  unsigned int length = udp.parsePacket();
  if (length) {
    udp.read(buffer, min(length, HEIGHT));
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.write(buffer[0]);
    udp.endPacket();
  }
}
