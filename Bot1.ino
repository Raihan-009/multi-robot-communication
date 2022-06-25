#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

#define ENA   14          // Enable/speed motors Right        GPIO14(D5)
#define ENB   12          // Enable/speed motors Left         GPIO12(D6)
#define IN_1  15          // L298N in1 motors RightP          GPIO15(D8)
#define IN_2  13          // L298N in2 motors RightN           GPIO13(D7)
#define IN_3  2           // L298N in3 motors LeftP            GPIO2(D4)
#define IN_4  0           //L298N in4 motors LeftN            GPIO0 (D3)
 
const char* ssid = "Banyan_House_Nestor";        // Enter your WiFi name
const char* password =  "banyan@sbn";   // Enter WiFi password
const char* mqttServer = "36.255.69.54";  // Enter Server Ip
const int mqttPort = 1883;        // Port
const char* mqttUser = "";
const char* mqttPassword = "";
 
WiFiClient espClient;
PubSubClient client(espClient);

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

// Variable to save current epoch time
double epochTime;
 
void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);  
  pinMode(IN_1, OUTPUT);
  pinMode(IN_2, OUTPUT);
  pinMode(IN_3, OUTPUT);
  pinMode(IN_4, OUTPUT);
  
  Serial.begin(115200);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {
 
      Serial.println("connected");  
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
  }
 
  client.subscribe("bot1");
 
}

  // Function that gets current epoch time
  double getTime() {
  timeClient.update();
  double now = timeClient.getEpochTime();
  return now;
}

void forward(){
  digitalWrite(IN_1, LOW);
  digitalWrite(IN_2, HIGH);
  analogWrite(ENA, 100);

  digitalWrite(IN_3, LOW);
  digitalWrite(IN_4, HIGH);
  analogWrite(ENB, 100);
}


void _stop(){
  digitalWrite(IN_1, LOW);
  digitalWrite(IN_2, LOW);
  analogWrite(ENA, 0);

  digitalWrite(IN_3, LOW);
  digitalWrite(IN_4, LOW);
  analogWrite(ENB, 0);
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.println("*************************");
  
  if (((char)payload[0]) == 'f'){Serial.println("Done");forward();delay(2000);_stop();}
  Serial.println((char)payload[0]);
  epochTime = getTime();
  Serial.print("Epoch Time: ");
  Serial.println(epochTime);

  Serial.println("*************************");
  Serial.println();
}
void loop() {
  client.loop();
}