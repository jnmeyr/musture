#include "network.hpp"

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "display.hpp"

WiFiServer tcpServer(50000);
WiFiUDP udp;
unsigned int lastCount = 0;

void setupNetwork() {
  WiFi.mode(WIFI_STA);
  WiFi.begin("", "");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }

  tcpServer.begin();
  udp.begin(50001);
}

void readControls(char * controls) {
  WiFiClient tcpClient = tcpServer.available();
  if (tcpClient && tcpClient.connected()) {
    for (int index = 0; index < 4; index++) {
      controls[index] = tcpClient.read();
    }
    tcpClient.stop();
  }
}

void readValues(char * values) {
  unsigned int length = udp.parsePacket();
  if (length) {
    udp.read(values, min(length, HEIGHT));
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.write(values[0]);
    udp.endPacket();
  }
}
