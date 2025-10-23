#define sprint Serial.print
#define sprintln Serial.println
#include <IRremote.hpp> // IRremote 4.1.2 from Library Manager
int RECV_PIN = 11;

unsigned long timeBegin;
int c = 1;

void setup()
{
  Serial.begin(9600);
  IrReceiver.begin(RECV_PIN, ENABLE_LED_FEEDBACK); // Start the receiver
  timeBegin = micros();
}

void loop() {
  if (IrReceiver.decode()) {
    dump();
// ========
    Serial.println(IrReceiver.decodedIRData.decodedRawData, HEX);
    Serial.print("rawlen ");
    Serial.println(IrReceiver.decodedIRData.rawDataPtr->rawlen);
    Serial.print("decode type ");
    Serial.println(IrReceiver.decodedIRData.protocol);

    unsigned long timeEnd = micros();
    unsigned long duration = timeEnd - timeBegin;
    double averageDuration = (double)duration / 1000.0;
    Serial.println(averageDuration);
//    if(IrReceiver.decodedIRData.decodedRawData==0xA1026EFF) {
//      Serial.println("turning off");
//    }
    IrReceiver.resume(); // Receive the next value
  }
}

void dump() {
   int count = IrReceiver.decodedIRData.rawDataPtr->rawlen;
   sprintln(c);
   c++;
   sprintln("For IR Scope: ");
   for (int i = 1; i < count; i++) {
       sprint("0x");
       sprint((unsigned int)IrReceiver.decodedIRData.rawDataPtr->rawbuf[i] * MICROS_PER_TICK, HEX);
    sprint(" ");
   }

   sprintln("");
   sprintln("For Arduino sketch: ");
   sprint("uint16_t raw[");
   sprint(count, DEC);
   sprint("] = {");
   for (int i = 1; i < count; i++) {
       sprint("0x");
       sprint((unsigned int)IrReceiver.decodedIRData.rawDataPtr->rawbuf[i] * MICROS_PER_TICK, HEX);
       sprint(",");
    }
    sprint("};");
    sprintln("");
    sprint("IrSender.sendRaw(raw,");
    sprint(count, DEC);
    sprint(",38);");
    sprintln("");
    sprintln("");
}
