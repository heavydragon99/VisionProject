#include <Wire.h>
#include <Zumo32U4.h>

const int toNicla = 13;
const int fromNicla = 14;
const int receivePin = 7;
const int sendPin = 4;
const int led = LED_BUILTIN;
Zumo32U4Motors motors;
int inputValue;
int motorValue; //msb t/m 4 is voor motor, 3 t/m lsb is voor borden
int bits[8] = {0,0,0,0,0,0,0,0};

int checkSilence()  //Check wheter no messages are currently being received
{
  int canstart=0;
  inputValue = digitalRead(fromNicla);
  if (inputValue == HIGH)
  {
    delay(50);
    canstart=1;
  }
  else
  {
    canstart=0;
  }
  inputValue = digitalRead(fromNicla);
  if (inputValue == HIGH && canstart == 1)
  {
    delay(50);
    canstart=1;
  }
  else
  {
    canstart=0;
  }
  inputValue = digitalRead(fromNicla);
  if (inputValue == HIGH && canstart == 1)
  {
    return 0;
  }
  return 1;
}

void requestData()
{
  digitalWrite(toNicla,HIGH); //ready to receive
  digitalWrite(led,HIGH);
}

void waitForStart()
{
  while (digitalRead(fromNicla) == 1) {
  //while (1){
    //Serial.println(digitalRead(fromNicla));
    ledRed(digitalRead(fromNicla));
  }
  //Serial.println("Startbit");
}

int receiveByte()
{
  digitalWrite(toNicla,LOW); //NOT READY TO RECEIVE
  digitalWrite(led,LOW);
  delay(25); //Go to halfway through the startbit
  motorValue = 0;
  for (int i = 0; i < 8; i++)
  {
    delay(50);
    int inputValue = digitalRead(fromNicla);
    //Serial.print(inputValue);
    motorValue |= ((1&inputValue) << i);
  }
  
  return motorValue;
}

void processCommand(unsigned commandValue)
{
  switch (commandValue)
  {
    case 0:
      motors.setLeftSpeed(0);
      motors.setRightSpeed(0);
      break;
    case 1:
      motors.setLeftSpeed(150);
      motors.setRightSpeed(150);
      //vooruit
      break;
    case 2:
      motors.setLeftSpeed(50);
      motors.setRightSpeed(150);
      //links
      break;
    case 3:
      motors.setLeftSpeed(150);
      motors.setRightSpeed(50);
      break;
    default:
      break;
  }
}

void setup() {
  Serial.begin(9600);
  //Serial.println("Startup");
  pinMode(receivePin,INPUT);
  pinMode(sendPin,OUTPUT);
  pinMode(led,OUTPUT);
  pinMode(toNicla,OUTPUT);
  pinMode(fromNicla,INPUT_PULLUP);
  digitalWrite(toNicla,LOW);
  digitalWrite(led,HIGH);
  motorValue = 0;
}

/////////////TO DO: ZORGEN DAT ER EEN TWEEDE LIJN KOMT DIE DATA REQUEST
void loop() {
//  while(checkSilence())
//  {
//  }
  ////delay(5000);
  //Serial.println("request now");
  requestData();
  waitForStart();
  receiveByte();
  //Serial.println();
  Serial.println(motorValue);
  processCommand(motorValue / 16);
  delay(50);
  
}
