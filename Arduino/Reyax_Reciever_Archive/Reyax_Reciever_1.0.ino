#include <SoftwareSerial.h>

String IncomingString;
String AT_Cmd;

SoftwareSerial lora_serial(2, 3); // RX, TX

String FREQUENCY_BAND = "433000000";
String NETWORK_ID = "7";              // Recommended 1~15
String NODE_ADDRESS_NATIVE = "2";
String NODE_ADDRESS_FOREIGN = "1";

bool Flip = true;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600); delay(1000);
  Serial.println("Starting Reyax Receiver");

  lora_serial.begin(9600); delay(1000);
  lora_serial.println("AT+IPR=9600");delay(1000);
  lora_serial.println("AT+BAND="+ FREQUENCY_BAND); delay(1000);
  lora_serial.println("AT+NETWORKID="+ NETWORK_ID); delay(1000);
  lora_serial.println("AT+ADDRESS="+ NODE_ADDRESS_NATIVE);  delay(1000);
  lora_serial.println("AT+PARAMETER= 10,7,1,7"); delay(1000);
  //lora_serial.println("AT+CPIN=FABC0002EEDCAA90FABC0002EEDCAA90"); delay(1000);

  Serial.println("Process Initialized");
}

void loop() {

  while (lora_serial.available()) {
    \\IncomingString = lora_serial.readString();
    IncomingString = lora_serial.readStringUntil('\n');
    if(IncomingString.length() > 2){
      Serial.print("Receiver incoming: "); Serial.println(IncomingString);
      Serial.print("String Length: "); Serial.println(String(IncomingString.length()));

      int s = IncomingString.indexOf("["); int e = IncomingString.indexOf("]");
      Serial.print (String(s));
      Serial.print (String(e));
      Serial.println (IncomingString.substring(s,e));
      Serial.println("---------------------------------------------------------------");

      String Message = "Thanks received :"; // + ((s > 0 and e > 0) ? IncomingString.substring(s,e) : "");

      AT_Cmd = "AT+SEND=" + NODE_ADDRESS_FOREIGN + ",";
      AT_Cmd += String(Message.length() - 2);
      AT_Cmd += "," + Message;

      Serial.print("Receiver outgoing: "); Serial.println(AT_Cmd);
      lora_serial.println(AT_Cmd);
    }
  }

  digitalWrite(LED_BUILTIN, HIGH); delay(1000); digitalWrite(LED_BUILTIN, LOW);
}
