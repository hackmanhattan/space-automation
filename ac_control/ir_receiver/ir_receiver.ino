#define sprint Serial.print 
#define sprintln Serial.println
#include <IRremote.h>
int RECV_PIN = 11;


IRrecv irrecv(RECV_PIN);


decode_results results;
int c = 1;

void setup()
{
  Serial.begin(9600);
  irrecv.enableIRIn(); // Start the receiver
}

void loop() {


  if (irrecv.decode(&results)) {
   dump(&results);
// ========
    Serial.println(results.value, HEX);
    Serial.print("rawlen ");
    Serial.println(results.rawlen);
    Serial.print("decode type ");
    Serial.println(results.decode_type);
    if(results.value==0xA1026EFF) {
      Serial.println("turning off");
    }
    irrecv.resume(); // Receive the next value

  }
}

void dump(decode_results *results) {
   int count = results->rawlen;
   sprintln(c);
   c++;
   sprintln("For IR Scope: ");
   for (int i = 1; i < count; i++) {
       sprint("0x");
       sprint((unsigned int)results->rawbuf[i], HEX);
    sprint(" ");
   }

   sprintln("");
   sprintln("For Arduino sketch: ");
   sprint("unsigned int raw[");
   sprint(count, DEC);
   sprint("] = {");
   for (int i = 1; i < count; i++) {
       sprint("0x");
       sprint((unsigned int)results->rawbuf[i], HEX);
       sprint(",");
    }
    sprint("};");
    sprintln("");
    sprint("irsend.sendRaw(raw,");
    sprint(count, DEC);
    sprint(",38);");
    sprintln("");
    sprintln("");
}
