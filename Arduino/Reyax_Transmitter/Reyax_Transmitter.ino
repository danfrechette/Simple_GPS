/*************************************************************************************************
 *  Created By: Tauseef Ahmad
 *  Created On: 20 July, 2023
 *  
 *  YouTube Video: https://youtu.be/390JbyaBIjg
 *  My Channel: https://www.youtube.com/@AhmadLogs
 ***********************************************************************************************/
#include <SoftwareSerial.h>
SoftwareSerial lora_serial(2, 3); // RX, TX

String FREQUENCY_BAND = "433000000";
String NETWORK_ID = "7";
String THIS_DEVICE = "1";
String OTHER_DEVICE = "2";
int cntr =0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.begin(115200); delay(1000);
  Serial.println("Starting Reyax Transmitter");
  
  lora_serial.begin(115200); delay(1000);
  lora_serial.println("AT+BAND=" + FREQUENCY_BAND); delay(1000);
  lora_serial.println("AT+NETWORKID=" + NETWORK_ID); delay(1000);
  lora_serial.println("AT+ADDRESS=" + THIS_DEVICE); delay(1000);
  
  Serial.println("Process Initialized"); 
}

void loop() {
  
  String AT_Cmd = F("AT+SEND=2,14,Test Message A");
  digitalWrite(LED_BUILTIN, HIGH);  
  
  
  lora_serial.println(AT_Cmd);
  Serial.println(AT_Cmd);
  
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  
}
