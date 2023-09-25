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
String THIS_DEVICE = "2";
String OTHER_DEVICE = "1";
bool Flip = true;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.begin(115200); 
  delay(1000);
  Serial.println("Starting Reyax Reciever");
  
  lora_serial.begin(115200); delay(1000);
  lora_serial.println("AT+BAND="+ FREQUENCY_BAND); delay(1000);
  lora_serial.println("AT+NETWORKID="+ NETWORK_ID); delay(1000);
  lora_serial.println("AT+ADDRESS="+ THIS_DEVICE);  delay(1000); 
  
  Serial.println("Process Initialized");
  digitalWrite(LED_BUILTIN, HIGH);
}

void loop() {
  if(Flip){
      Serial.println("Reading Lora_Serial. High");
  } else {
    Serial.println("Reading Lora_Serial. Low");
  }
  
  while (lora_serial.available()) { 
    String data = lora_serial.readString();
    Serial.println("Data:" + data);
  }  
  
  digitalWrite(LED_BUILTIN, Flip == true ? HIGH : LOW);
  Flip = Flip ? false : true;
  
  delay(1000);
}

//  if (digitalRead(buttonPin) == LOW){ 
//    relayState = !relayState;
//    String command = (relayState == true) ? "a1" : "a0";
//    lora_serial.println(
//      "AT+SEND="+ OTHER_DEVICE+",2,"+ command);
//    Serial.println(command);
//    delay(500); //debounce handling
//  }    
//    if(data.indexOf("a1") > 0) { 
//      digitalWrite(ledPin, HIGH);
//      relayState = 1;
//    } else if(data.indexOf("a0") > 0) { 
//      digitalWrite(ledPin, HIGH);
//      relayState = 0;
//    }
