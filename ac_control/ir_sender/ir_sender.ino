#include <IRremote.h>

int SEND_PIN = 3;
IRsend irsend(SEND_PIN);

  uint32_t off_code = 0xA1026EFF;
    uint32_t on_code = 0xA1826EFF;
  uint8_t code_len = 32;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("initiated");
}

void loop() {
  // put your main code here, to run repeatedly:

irsend.sendNEC(off_code,code_len);
delay(5000);
irsend.sendNEC(on_code,code_len);
delay(5000);
}
