//// ****** THIS FILE IS AUTOGENERATED ******
////
////          >>>> PLEASE ADAPT IT TO YOUR NEEDS <<<<
////
/// 
///  Filename; C:\Users\Agus\Desktop\driver.py
///  Source class: BotellaLoca
///  Generation timestamp: 2018-11-28T18:04:33.919448
///  Class code hash: 502e5622f90432aab452ee90e4cdbccaabe7b8d8
///
/////////////////////////////////////////////////////////////



#include "inodriver_user.h"

#define DIR  8
#define STEP  9

void user_setup() {
  pinMode(DIR, OUTPUT);
  pinMode(STEP, OUTPUT);
  digitalWrite(DIR,HIGH);

  set_PASO(50);
  delay(100);
  set_PASO(100);
  delay(100);
  set_PASO(-100);
}

void user_loop() {
}
// COMMAND: PASO, FEAT: paso
int set_PASO(int value) {
   if (value<0) {
    digitalWrite(DIR,LOW);
   } else {
    digitalWrite(DIR,HIGH);
   }
   for (int i = 0 ; i < abs(value) ; i++) 
    {
      digitalWrite(STEP,HIGH);
      delay(10);
      digitalWrite(STEP,LOW);
      delay(10);
    }  
  return value;
};
