#include <ArduinoJson.h>
#include <WiFi.h>
#include <WiFiUdp.h>



/* WiFi network name and password */
const char * ssid = "Bab:pepep";
const char * pwd = "boisudahtiada";

// IP address to send UDP data to.
// it can be ip address of the server or
// a network broadcast address
// here is broadcast address
const char * udpAddress = "192.168.100.255"; //mengikuti IP Address local
const int udpPort = 8888;

//create UDP instance
WiFiUDP udp;

void setup() {
  Serial.begin(115200);

  //Connect to the WiFi network
  WiFi.begin(ssid, pwd);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  //This initializes udp and transfer buffer
  udp.begin(udpPort);
}
float def_Volt = 220.0;
float def_Current = 5.0;
float def_kwh = 0.55;
float def_Power = 1100.0;
float def_cosphi = 1.0;
float def_Frequency = 50.0;
float data = 0;
String json()
{
  const size_t capacity = 6 * JSON_ARRAY_SIZE(3) + JSON_OBJECT_SIZE(6);
  DynamicJsonDocument doc(capacity);
  JsonArray volt = doc.createNestedArray("volt");
  volt.add(def_Volt+((float)random(0,100)/10));
  volt.add(def_Volt+((float)random(0,100)/10));
  volt.add(def_Volt+((float)random(0,100)/10));

  JsonArray current = doc.createNestedArray("current");
  current.add(def_Current+((float)random(0,20)/10));
  current.add(def_Current+((float)random(0,20)/10));
  current.add(def_Current+((float)random(0,20)/10));

  JsonArray kwh = doc.createNestedArray("kwh");
  kwh.add(def_kwh+((float)random(0,2)/10));
  kwh.add(def_kwh+((float)random(0,2)/10));
  kwh.add(def_kwh+((float)random(0,2)/10));

  JsonArray power = doc.createNestedArray("power");
  power.add(def_Power+((float)random(0,200)/10));
  power.add(def_Power+(float)(random(0,200)/10));
  power.add(def_Power+((float)random(0,200)/10));

  JsonArray cosphi = doc.createNestedArray("cosphi");
  cosphi.add(def_cosphi-((float)random(0,5)/10));
  cosphi.add(def_cosphi-((float)random(0,5)/10));
  cosphi.add(def_cosphi-((float)random(0,5)/10));

  JsonArray frequency = doc.createNestedArray("frequency");
  frequency.add((float)def_Frequency);
  frequency.add((float)def_Frequency);
  frequency.add((float)def_Frequency);
  // data++;
  // if(data > 99) data =0;
  String jos;

  serializeJson(doc, jos );
  Serial.println(jos);
  return jos;
}

int n = 0;
void loop() {
  //data will be sent to server
//  json();
  n++;
  byte sas;
  int integer = 12412416;
  String Str = json();
  String st = "ESP32 Kirim";
  Serial.println(Str.length());
  int Lndata = Str.length() + 1;
  byte buffer[Lndata];
  Str.getBytes(buffer, Lndata);

  //for(int i = 0; i < 50; i++){
  //     buffer[i] = integer % 10;  // remainder of division with 10 gets the last digit
  //     integer /= 10;     // dividing by ten chops off the last digit.
  //}

  //send hello world to server
  udp.beginPacket(udpAddress, udpPort);
  udp.write(buffer, Lndata);
  udp.endPacket();
  memset(buffer, 0, Lndata);
  //processing incoming packet, must be called before reading the buffer
  udp.parsePacket();
  //receive response from server, it will be HELLO WORLD
  if (udp.read(buffer, Lndata) > 0) {
    Serial.print("Server to client: ");
    Serial.println((char *)buffer);
  }
  //Wait for 1 second
  delay(700);
}