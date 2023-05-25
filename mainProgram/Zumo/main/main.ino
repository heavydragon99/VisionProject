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

int countLoops = 0;
int ReceivedValue = 0;

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

bool waitForStart()
{
  int timeout = 0;
  while (digitalRead(fromNicla) == 1) {
    if(timeout == 10000)
    {
      Serial.println("timeout");
      return false;
    }
    ledRed(digitalRead(fromNicla));
    timeout++;
  }
  return true;
}

int receiveByte()
{
  digitalWrite(toNicla,LOW); //NOT READY TO RECEIVE
  digitalWrite(led,LOW);
  delay(5); //Go to halfway through the startbit
  motorValue = 0;
  for (int i = 0; i < 8; i++)
  {
    delay(10);
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
      motors.setLeftSpeed(100);
      motors.setRightSpeed(100);
      //vooruit
      break;
    case 2:
      motors.setLeftSpeed(50);
      motors.setRightSpeed(75);
      //links
      break;
    case 3:
      motors.setLeftSpeed(75);
      motors.setRightSpeed(50);
      break;
    case 4:
      motors.setLeftSpeed(0);
      motors.setRightSpeed(150);
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
  delay(1000);
}

/////////////TO DO: ZORGEN DAT ER EEN TWEEDE LIJN KOMT DIE DATA REQUEST
void loop() {
  
//  while(checkSilence())
//  {
//  }
  //delay(5000);
  //Serial.println("request now");
  requestData();
  bool checkStart = waitForStart();

  if(checkStart)
  {
    Serial.println("receive");
    receiveByte();
    if(motorValue != 255)
    {
      ReceivedValue = motorValue;
    }
    countLoops = 0;
  }
  
  //Serial.println();

  Serial.println("countLoops-");
  Serial.println(countLoops);
  if(countLoops < 10)
  {
      Serial.println("motorValue-");
      Serial.println(ReceivedValue);
    processCommand(motorValue);
  }
  else
  {
    processCommand(0); 
  }
   
  //delay(50);
  countLoops++;
}
