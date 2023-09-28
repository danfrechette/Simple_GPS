#include <SoftwareSerial.h>

String Lora_Message(Sting Msg){
  String AT_Cmd = "AT+SEND=" + NODE_ADDRESS_FOREIGN + ",";
  AT_Cmd += String(Msg.length()) + "," + Msg;
  return AT_Cmd
}

#define rxPin 3
#define txPin 2
SoftwareSerial lora_serial(rxPin, txPin);

String IncomingString;
String AT_Cmd;
String FREQUENCY_BAND="433000000";
String NETWORK_ID="7";
String NODE_ADDRESS_NATIVE="1";
String NODE_ADDRESS_FOREIGN="2";
int Cntr = 0;

void setup() {
  pinMode(rxPin, INPUT); pinMode(txPin, OUTPUT);

  Serial.begin(9600); while(!Serial);
  Serial.println("Started Arduino Serial Connection.");

  lora_serial.begin(9600); delay(1000);
  Serial.println("\tStarted Reyax Serial Connection @ 155200 Baud Rate.");
    lora_serial.begin(115200); delay(1000);
    lora_serial.println("AT+IPR=9600"); delay(1000);

  Serial.println("\tResetting Reyax Transmitter to 9600 Baud Rate.");
    lora_serial.begin(9600); delay(1000);

  Serial.print("\tConfiguring Reyax Module"); delay(1000); Serial.print(".");
    lora_serial.println("AT+BAND=" + FREQUENCY_BAND); delay(1000); Serial.print(".");
    lora_serial.println("AT+NETWORKID=" + NETWORK_ID); delay(1000); Serial.print(".");
    lora_serial.println("AT+ADDRESS=" + NODE_ADDRESS_NATIVE); delay(1000); Serial.print(".");
    lora_serial.println("AT+IPR=9600"); delay(1000); Serial.print(".");
    lora_serial.println("AT+PARAMETER=10,7,1,7");delay(1000); Serial.print(".");
    lora_serial.println("AT+CPIN=FABC0002EEDCAA90FABC0002EEDCAA90"); delay(1000); Serial.println(".");
    IncomingString = lora_serial.readString(); Serial.print(IncomingString);

  Serial.print("\tGathering Reyax Settings "); delay(1000);
    lora_serial.println("AT+BAND?"); delay(1000); Serial.print(".");
    lora_serial.println("AT+NETWORKID?"); delay(1000); Serial.print(".");
    lora_serial.println("AT+ADDRESS?"); delay(1000); Serial.print(".");
    lora_serial.println("AT+IPR?"); delay(1000); Serial.println(".");
    IncomingString = lora_serial.readString(); Serial.print(IncomingString);
    lora_serial.println("AT+CPIN?"); delay(1000); Serial.print(".");
    lora_serial.println("AT+PARAMETER?"); delay(1000); Serial.println(".");
    IncomingString = lora_serial.readString(); Serial.print(IncomingString);

  Serial.print("\tTransmitter Send Message Test: "); delay(1000);
    lora_serial.println(Lora_Message("HELLO")); delay(1000);
    IncomingString = lora_serial.readString(); Serial.print(IncomingString);
    delay(1000);

  Serial.println("Process Initialized");
}

void loop() {
  AT_Cmd = Lora_Message("Outgoing Message[" + String(++Cntr) + "]");
  Serial.print("\tOut-going -> : "); Serial.println(AT_Cmd);
  lora_serial.println(AT_Cmd); delay(1000);

  while (lora_serial.available()) {
    IncomingString = lora_serial.readStringUntil('\n');
    if(IncomingString.length() > 2){

      if(stringOne.startsWith("+RCV=")){
        Serial.print("\tIncoming Message: "); Serial.println(IncomingString);
      }
      else {
        Serial.print("\t"); Serial.println(IncomingString);
      }
    }

    delay(1000);
  }
}

