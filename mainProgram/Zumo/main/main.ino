#include <Wire.h>
#include <Zumo32U4.h>

const int toNicla = 13;
const int fromNicla = 14;
const int receivePin = 7;
const int sendPin = 4;
const int led = LED_BUILTIN;
Zumo32U4Motors motors;
Zumo32U4Encoders encoders;
Zumo32U4OLED display;
int inputValue;
int motorValue;
int bits[8] = {0,0,0,0,0,0,0,0};

int countLoops = 0;
int ReceivedValue = 0;

bool checkStoplicht = false;

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
      //Serial.println("timeout");
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
   
//   Serial.println("--commandValue--");
//   Serial.println(commandValue);
   //normal driving
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
   //intersection handeling
   else if(commandValue == 4)
   {
    display.clear();
    display.print("turn");
    display.gotoXY(0,1);
    display.print("left");
    turn(-90);
   }
   else if(commandValue == 5)
   {
    display.clear();
    display.print("turn");
    display.gotoXY(0,1);
    display.print("right");
    turn(90);
   }
   //signs
   else if(commandValue == 6)//stop bord
   {
    display.clear();
    display.print("Stopbord");
    motors.setSpeeds(0, 0);
    delay(3000);
   }
   else if(commandValue == 7)//verboden in rijden
   {
    display.clear();
    display.print("verboden");
    display.gotoXY(0,1);
    display.print("rijden");
    drive(2000);
    turn(172);
   }
   else if(commandValue == 8)//verboden auto
   {
    display.clear();
    display.print("verboden");
    display.gotoXY(0,1);
    display.print("auto");
    drive(2000);
    turn(-172);
   }
   else if(commandValue == 9)//50 bord
   {
    display.clear();
    display.print("bord 50");
    motors.setSpeeds(50, 50);
   }
   //traffic lights
   else if(commandValue == 10)//rood
   {
    checkStoplicht = true;
    display.clear();
    display.print("stoplicht");
    display.gotoXY(0,1);
    display.print("rood");
    motors.setSpeeds(0, 0);
    delay(3000);
   }
   else if(commandValue == 11)//geel
   {
    display.clear();
    display.print("stoplicht");
    display.gotoXY(0,1);
    display.print("geel");
    motors.setSpeeds(100, 100);
   }
   else if(commandValue == 12)//groen
   {
    display.clear();
    display.print("stoplicht");
    display.gotoXY(0,1);
    display.print("groen");
    motors.setSpeeds(100, 100);
   }
   //intersection handeling
   else if(commandValue > 180 && commandValue <= 190)  // turn right
   {
    motors.setSpeeds(125, -125);
    delay(commandValue-180);
    motors.setSpeeds(0, 0);
   }

   else if(commandValue > 190 && commandValue <= 200) // turn left
   {
    motors.setSpeeds(-125, 125);
    delay(commandValue-190);
    motors.setSpeeds(0, 0);
   }
   
   else if(commandValue > 200 && commandValue <= 255)
   {
    display.clear();
    display.print("intersection");
    display.gotoXY(0,1);
    display.print((commandValue-200));
    int count = commandValue -200;
    count = count*55;
    drive(count);
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
  display.clear();
  display.print("Starting");
  delay(1000);

}

void loop() {
//  display.clear();
//  display.print("Running");
  requestData();
  bool checkStart = waitForStart();

  if(checkStart)
  {
    //Serial.println("receive");
    receiveByte();
    if(motorValue != 255 and motorValue != 224)
    {
      ReceivedValue = motorValue;
    }
    countLoops = 0;
  }
//  Serial.println("countLoops-");
//  Serial.println(countLoops);
//  Serial.println("ReceivedValue-");
//  Serial.println(ReceivedValue);
  if(countLoops < 8 and checkStoplicht == false)
  {
    Serial.println("hierin1");
      Serial.println(ReceivedValue);
    processCommand(ReceivedValue);
  }
  else
  {
    if(checkStoplicht == true && ReceivedValue == 12)
    {
      Serial.println("hierin2");
      Serial.println(ReceivedValue);
      checkStoplicht = false;
      processCommand(ReceivedValue);
    }
    else
    {
      processCommand(0); 
    }
  }
   
  //delay(50);
  countLoops++;
}
