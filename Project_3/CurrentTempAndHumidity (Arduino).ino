#include <WiFi.h>
#include <HttpClient.h>
#include <LiquidCrystal.h>
#include <ArduinoJson.h>

// Local WIFI network credentials
char ssid[] = "?";         // your network SSID (name)
char pass[] = "?";         // your network password
int status = WL_IDLE_STATUS;       // the WiFi radio's status

// IP address of the Raspberry Pi on the same network
const char* serverIP = "?";
const int serverPort = 8000;

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

WiFiClient client;
HttpClient http(client, serverIP, serverPort);

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi connected");

  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("Starting...");
  delay(1000);
}

void loop() {
  String url = "/data";

  http.get(url);
  int statusCode = http.responseStatusCode();
  String response = http.responseBody();
  Serial.print("Status Code: ");
  Serial.println(statusCode);
  Serial.print("Response: ");
  Serial.println(response);

  String jsonString = String(response);

  // set the cursor to column 0, line 1
  // (note: line 1 is the second row, since counting begins with 0):
  lcd.clear();
  lcd.setCursor(0, 0);

  if (statusCode == 200) {
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, response);
    if (error) {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.f_str());
      String serror = error.f_str();
      lcd.print("Json Error: " + serror);
    } else {
      const char* ctemp = doc["temperature"];
      String temp = String(ctemp);
      lcd.print("Tem: " + temp);

      lcd.setCursor(0, 1);
      const char* chum = doc["humidity"];
      String hum = String(chum);
      lcd.print("Hum: " + hum);

      lcd.setCursor(11, 0);
      const char* ctime = doc["time"];
      String stime = String(ctime);
      lcd.print(stime);
    }
  } else {
    lcd.print("Http Error: " + String(statusCode) + " " + jsonString);
  }

  delay(60000);
}
