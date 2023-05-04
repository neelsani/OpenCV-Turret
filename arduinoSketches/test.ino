#include <Servo.h>
Servo myservo;
int pos = 0;



void setup()

{

Serial.begin(9600);
while (!Serial);
Serial.println("-------------------------");
Serial.println("ARos is loading....");
delay(1000);
Serial.println("ARos loaded succesfully");
Serial.println("-------------------------");
myservo.attach(9);
Serial.println("calibrating servo...");
for(pos = 0; pos <= 180; pos += 1)
myservo.write(0);
delay(1000);
myservo.write(180);
delay(1000);
myservo.write(90);
delay(1000);
Serial.println("servo calibrated");
Serial.println("-------------------------");
Serial.println("Comand input online, write command to perform action");
Serial.println("-------------------------");

}

void loop() {
  
for(pos = 0; pos <= 180; pos += 1)
if (Serial.available())


{
  int state = Serial.parseInt();
    
if (state < 10)

{
Serial.print(">");
Serial.println(state);
Serial.println("cannost execute command, too low number");

}

if (state >= 10 && state < 170)
{
  Serial.print(">");
  Serial.println(state);
  Serial.print("turning servo to ");
  Serial.print(state);
  Serial.println(" degrees");
  myservo.write(state);
  
}

}

}
