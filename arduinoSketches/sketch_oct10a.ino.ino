//Arduino Code

#include <Servo.h>

Servo myServo;  // create servo object to control a servo
int pos = 90;    // variable to store the servo position
String inString = "";    // string to hold input

void setup() {
  myServo.attach(9);
  // Open serial communications and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // send an intro:
  Serial.println("\n\nString toInt():");
  Serial.println();
}

void loop() {
  // Read serial input:
  while (Serial.available() > 0) {
    int inChar = Serial.read();
    if (isDigit(inChar)) {
      // convert the incoming byte to a char
      // and add it to the string:
      inString += (char)inChar;
    }
    // if you get a newline, print the string,
    // then the string's value:
    if (inChar == '\n') {
      Serial.print("Value:");
      Serial.println(inString.toInt());
      Serial.print("String: ");
      Serial.println(inString);

      myServo.write(inString.toInt());
      // clear the string for new input:
      inString = "";
    }
  }
}
