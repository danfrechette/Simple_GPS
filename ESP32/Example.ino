/* LoRa transmitter - receiver messenger -- llcoder 11-18-2021
* There are three serial ports on the ESP known as U0UXD, U1UXD and U2UXD.
*
* U0UXD is used to communicate with the ESP32 for programming and during reset/boot.
* U1UXD is unused and can be used for your projects. Some boards use this port for SPI Flash access though
* U2UXD is unused and can be used for your projects.
*/


#define RXD2 16   // LoRa TX (ESP32 RX2)
#define TXD2 17   // LoRa RX (ESP32 TX2)


#include<LoRa.h>


String incomingString;
String PrStr;                                           // String used to print the incoming string after decoding it


void setup() {
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);  // (ESP32 UART)
}


void loop() {
  if (Serial.available()){
        incomingString = Serial.readString();
          if(incomingString.length()>2){
          Serial.print("YOU: ");
          Serial.println(incomingString);
          String messStr = "AT+SEND=0,";              // messStr(AT COMMAND) is to be sent to the LoRa module to send the relevant data
          messStr += (incomingString.length()-2);
          messStr += ",";
          messStr += incomingString;
          Serial2.print(messStr);
          }
    }


   else if (Serial2.available()){                  // this will read the incoming data from the lora and decode it and print it on serial monitor
        incomingString = Serial2.readString();
        String recTest = incomingString.substring(1,4);
        if(recTest == "RCV"){
        String messagesize;
        int addr_start = incomingString.indexOf(',');
        int addr_mid = incomingString.indexOf(',', addr_start + 1);
        messagesize = incomingString.substring(addr_start + 1, addr_mid);
        PrStr = incomingString.substring(addr_mid + 1, (addr_mid + 1 + messagesize.toInt()));
        Serial.print("THEM: ");
        Serial.println(PrStr);
        }
    }
}