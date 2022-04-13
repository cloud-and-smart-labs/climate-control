#include <Servo.h>

Servo myservo_1;
Servo myservo_2;
int pos_1;
int pos_2;

void setup()
{
  myservo_1.attach(9);
  myservo_2.attach(10);
  Serial.begin(9600);
  while (!Serial)
    ;
}

void loop()
{
  while (Serial.available())
  {
    pos_1 = Serial.parseInt();
//    Serial.print("Sevo-1:");
//    Serial.println(pos_1);
    if(0<=pos_1 && pos_1 <=180)
      myservo_1.write(pos_1);
    
    pos_2 = Serial.parseInt();
//    Serial.print("Sevo-2:");
//    Serial.println(pos_2);
    if(0<=pos_2 && pos_2 <=180)
      myservo_2.write(pos_2);
  }
}
