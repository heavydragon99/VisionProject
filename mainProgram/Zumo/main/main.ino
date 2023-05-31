#include <Wire.h>
#include <Zumo32U4.h>

const int toNicla = 13;
const int fromNicla = 14;
const int receivePin = 7;
const int sendPin = 4;
const int led = LED_BUILTIN;
Zumo32U4Motors motors;
Zumo32U4Encoders encoders;
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

void turn(long degree) {
  encoders.getCountsAndResetLeft();
  encoders.getCountsAndResetRight();

  long countsLeft = 0;
  long countsRight = 0;
  long degreeToCount = 7;
  if(degree > 0)//turn right
  {
    int count = degree*degreeToCount;

    motors.setSpeeds(125, -125);
    while(countsLeft < count and countsRight < count) {
    countsLeft += encoders.getCountsAndResetLeft();
    countsRight += encoders.getCountsAndResetRight();
    delay(2);
  }
  }
  if(degree < 0)//turn left
  {
    int count = (degree*-1)*degreeToCount;
    motors.setSpeeds(-125, 125);
    while(countsLeft < count and countsRight < count) {
    countsLeft += encoders.getCountsAndResetLeft();
    countsRight += encoders.getCountsAndResetRight();
    delay(2);
  }
  
  }
  motors.setSpeeds(0, 0);
}

void drive(long count) {
  encoders.getCountsAndResetLeft();
  encoders.getCountsAndResetRight();

  long countsLeft = 0;
  long countsRight = 0;

  motors.setSpeeds(100, 100);
  while(countsLeft < count and countsRight < count) {
  countsLeft += encoders.getCountsAndResetLeft();
  countsRight += encoders.getCountsAndResetRight();
  delay(2);
  }
  motors.setSpeeds(0, 0);
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
  delay(1); //Go to halfway through the startbit
  motorValue = 0;
  for (int i = 0; i < 8; i++)
  {
    delay(2);
    int inputValue = digitalRead(fromNicla);
    //Serial.print(inputValue);
    motorValue |= ((1&inputValue) << i);
  }
  
  return motorValue;
}

void processCommand(unsigned commandValue)
{
   Serial.println("--commandValue--");
   Serial.println(commandValue);
   if(commandValue == 0)
   {
    motors.setSpeeds(0, 0);
   }
   else if(commandValue == 1)
   {
    motors.setSpeeds(100, 100);
   }
   else if(commandValue == 2)
   {
    motors.setSpeeds(75, 100);
   }
   else if(commandValue == 3)
   {
    motors.setSpeeds(100, 75);
   }
   else if(commandValue == 4)
   {
    turn(-90);
   }
   else if(commandValue == 5)
   {
    turn(90);
   }
   else if(commandValue > 200 && commandValue <= 255)
   {
    int count = commandValue -200;
    count = count*50;
    drive(count);
   }

  
//  switch (commandValue)
//  {
//   
//
//
//    
//    //follow lines
//    case 0:
//      motors.setLeftSpeed(0);
//      motors.setRightSpeed(0);
//      break;
//    case 1:
//      motors.setLeftSpeed(100);
//      motors.setRightSpeed(100);
//      //vooruit
//      break;
//    case 2:
//      motors.setLeftSpeed(75);
//      motors.setRightSpeed(100);
//      //links
//      break;
//    case 3:
//      motors.setLeftSpeed(100);
//      motors.setRightSpeed(75);
//      break;
//    // intersection handeling
//    case 4:
//      turn(-90);
//      break;
//    case 5:
//      turn(90);
//      break;
//    case :
//      drive(200);
//      break;
//    default:
//      break;
//  }
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
    processCommand(ReceivedValue);
  }
  else
  {
    processCommand(0); 
  }
   
  //delay(50);
  countLoops++;
}
