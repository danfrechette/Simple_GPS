#include <SoftwareSerial.h>

String IncomingString;
String AT_Cmd;

SoftwareSerial lora_serial(2, 3); // RX, TX

String FREQUENCY_BAND = "433000000";
String NETWORK_ID = "7";               // Recommended 1~15
String NODE_ADDRESS_NATIVE = "1";
String NODE_ADDRESS_FOREIGN = "2";
int Baudrate = 9600;

int Cntr = 0;

void setup() {
  // pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600); delay(1000);
  Serial.println("Starting Reyax Transmitter");

  lora_serial.begin(9600); delay(1000);
  lora_serial.println("AT+BAND=" + FREQUENCY_BAND); delay(1000);
  lora_serial.println("AT+NETWORKID=" + NETWORK_ID); delay(1000);
  lora_serial.println("AT+ADDRESS=" + NODE_ADDRESS_NATIVE); delay(1000);
  lora_serial.println("AT+IPR=9600");delay(1000);
  lora_serial.println("AT+PARAMETER=10,7,1,7");  delay(1000);
  lora_serial.println("AT+CPIN=FABC0002EEDCAA90FABC0002EEDCAA90"); delay(1000);

  Serial.println("Process Initialized");
}

void loop() {

  String Message = "Test Message[" + String(++Cntr) + "]";

  AT_Cmd = "AT+SEND=" + NODE_ADDRESS_FOREIGN + ",";
  AT_Cmd += String(Message.length() - 2);
  AT_Cmd += "," + Message;

  lora_serial.print(AT_Cmd); delay(1000);
  Serial.print("Transmitter outgoing: "); Serial.println(AT_Cmd);

  delay(1000);

  //while (lora_serial.available()) {
    // IncomingString = lora_serial.readString();
  //  IncomingString = lora_serial.readStringUntil('\n');
  //  if(IncomingString.length() > 2){
  //    Serial.print("Transmitter incoming: "); Serial.println(IncomingString);
  //  }
  //}

  // digitalWrite(LED_BUILTIN, HIGH); delay(1000); digitalWrite(LED_BUILTIN, LOW);
}
