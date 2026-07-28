#include "WiFi.h"
#include "camera_pins.h"

// Wi-Fi credentials
const char* ssid = "Your_SSID";
const char* password = "Your_PASSWORD";

void startCameraServer();
void setupLedFlash(int pin);

void setup() {
    Serial.begin(115200);
    Serial.setDebugOutput(true);
    Serial.println();

    WiFi.begin(ssid, password);
    int attempt = 0;

    while (WiFi.status() != WL_CONNECTED && attempt < 20) {
        delay(500);
        Serial.print(".");
        attempt++;
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("Wi-Fi Connected");
        Serial.print("IP Address: ");
        Serial.println(WiFi.localIP());

        startCameraServer();
    } else {
        Serial.println("Wi-Fi Connection Failed. Restarting...");
        ESP.restart();
    }
}

void loop() {
    // Main loop (can be extended for additional features)
}
