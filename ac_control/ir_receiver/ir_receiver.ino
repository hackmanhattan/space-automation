#define sprint Serial.print
#define sprintln Serial.println
#include <IRremote.hpp> // IRremote 4.4.1 from Library Manager

int RECV_PIN = 11;
unsigned long timeBegin;
int c = 1;

void setup()
{
  Serial.begin(9600);
  IrReceiver.begin(RECV_PIN, ENABLE_LED_FEEDBACK); // Start the receiver
  timeBegin = micros();
  Serial.println(F("Ready to receive IR signals"));
}

void loop() {
  if (IrReceiver.decode()) {
    // Print counter
    sprintln(c);
    c++;

    // Use built-in print functions from IRremote library
    IrReceiver.printIRResultShort(&Serial);
    Serial.println();

    // Print as C array for use in sender
    IrReceiver.printIRSendUsage(&Serial);

    // Additional details
    Serial.print("Protocol: ");
    Serial.println(IrReceiver.decodedIRData.protocol);
    Serial.print("Decoded value: 0x");
    Serial.println(IrReceiver.decodedIRData.decodedRawData, HEX);

    unsigned long timeEnd = micros();
    unsigned long duration = timeEnd - timeBegin;
    double averageDuration = (double)duration / 1000.0;
    Serial.println(averageDuration);

    IrReceiver.resume(); // Receive the next value
  }
}
