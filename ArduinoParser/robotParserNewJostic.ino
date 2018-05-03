#include <string.h>
#include <Servo.h>
#include <AFMotor.h>
#define SERVO_CAMERA 10
#define SERVO_PLATFORM 9

char unitID_in[10];
char X[10];
char Y[10];
char speadH[10];
char speadV[10];

long previousMillis = 0;   // здесь будет храниться время последнего изменения состояния светодиода 
long interval = 2000;      // интервал мигания в миллисекундах

int scanInt = 0;

Servo SCamera;
Servo SPlatform;
AF_DCMotor rMotor(1);
AF_DCMotor lMotor(2);


void setup() {
  // открываем порт
  Serial.begin(9600);
  SCamera.attach(SERVO_CAMERA);
  SPlatform.attach(SERVO_PLATFORM);

}

bool intervalMill()
{
  if (millis() - previousMillis > interval) 
  {
    previousMillis = millis();   // запоминаем текущее время
    // если светодиод был выключен – включаем и наоборот :)
    return true;
  }
  else
     return false;
}

void loop() {
 
  
  int i = 0;
  char buffer[100];

  //если есть данные - считаем их
  if (Serial.available())
  {
    delay(100);
    //сохраним прочитанное в буфер
    while ( Serial.available() && i < 99)
    {
      buffer[i++] = Serial.read();
    }

    //разобьем его на части, отделенные запятой

    sscanf(buffer, "%s %s %s %s %s", unitID_in, X, Y, speadH, speadV);
    Serial.flush();
  }
  
    
  

  //Исполнительная часть программы
  //Проверяем, к какому устройству пришли данные


  if ((String)unitID_in == "Pos") { //test serial read
    // Serial.print(buffer);
    Serial.print("X= ");
    Serial.println(X);
    Serial.print("Y= ");
    Serial.println(Y);

    String strX(X);
    String strY(Y);

    SCamera.write(strX.toInt());
    SPlatform.write(strY.toInt());

    unitID_in[0] = '\0';
  }
  if ((String)unitID_in == "Mot") { //test serial read

    Serial.print("nRightMotor = "); Serial.println(X);
    Serial.print("nLeftMotor = "); Serial.println(Y);

    Serial.print("SpeadRightMotor = "); Serial.println(speadH);
    Serial.print("SpeadLeftMotor = "); Serial.println(speadV);

    String nH(X);
    String nV(Y);
    String sH(speadH);
    String sV(speadV);

    int nR = nH.toInt();
    int nL = nV.toInt();
    int sR = sH.toInt();
    int sL = sV.toInt();

    if (nR == 0)
    {
      rMotor.run(RELEASE);
      Serial.println("RELEASE");
    }  
     else 
     if (nR == 1)
     {
      rMotor.run(FORWARD);
      Serial.println("FORWARD");
     }
     else 
     if (nR == -1)
     {
      rMotor.run(BACKWARD);
      Serial.println("BACKWARD");
     }

    if (nL == 0)
    {
      lMotor.run(RELEASE);
      Serial.println("RELEASE");
    }
    else 
    if (nL == 1) 
    {
      lMotor.run(FORWARD);
      Serial.println("FORWARD");
    }
    else 
    if (nL == -1)  
    {
      lMotor.run(BACKWARD);
      Serial.println("BACKWARD");
    }
    
    rMotor.setSpeed(sR);
    lMotor.setSpeed(sL);


    unitID_in[0] = '\0';
  }
}


















