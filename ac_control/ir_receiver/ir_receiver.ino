#include <IRremote.h>
int RECV_PIN = 11;


IRrecv irrecv(RECV_PIN);


decode_results results;

void setup()
{
  Serial.begin(9600);
  irrecv.enableIRIn(); // Start the receiver
}

void loop() {


  if (irrecv.decode(&results)) {
   
    Serial.println(results.value, HEX);
    
    if(results.value==0xA1026EFF) {
      Serial.println("turning off");
      irsend.sendNEC(off_code,off_code_len);
    }
    irrecv.resume(); // Receive the next value

  }
}

//
