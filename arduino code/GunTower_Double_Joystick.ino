#include <avr/wdt.h>
#include <PS2X_lib.h>  //for v1.6
#define deviceName "Arduin Nano: ATmega328P (Old Bootloader)"

// Function
#define SIGN(x) ((x) > 0 ? 1 : ((x) < 0 ? -1 : 0))


//++++++++++++++++++++++++++++++++++++++++++++++++++ Digital
  //++++++++++ Pin assignment
  const uint8_t TRIGGER_PIN = A3;
  const uint8_t LOCK_PIN = A2;

  //++++++++++ Variable  
  bool triggerState = false;
  bool pitchLock = false;


//++++++++++++++++++++++++++++++++++++++++++++++++++ Stepping
  //++++++++++ Pin assignment
  const uint8_t ENA_PIN[2] = {6, 9};      //[Yaw, Pitch]
  const uint8_t PUL_PIN[2] = {5, 8};      //[Yaw, Pitch]
  const uint8_t DIR_PIN[2] = {7, A0};     //[Yaw, Pitch]

  //++++++++++ Tunning
  unsigned long MAX_STEP_DELAY = 1500;
  unsigned long MIN_STEP_DELAY = 150;

  //++++++++++ Variable  
  long StepSpd[2] = {0};                  //[Yaw, Pitch]
  long StepCnt[2] = {0};                  //[Yaw, Pitch]
  bool StepState[2] = {0};                //[Yaw, Pitch]
  unsigned long StepTimer[2] = {0};       //[Yaw, Pitch]

//++++++++++++++++++++++++++++++++++++++++++++++++++ Protocol
  String numPart = "";

//++++++++++++++++++++++++++++++++++++++++++++++++++ Remote
PS2X ps2x; // create PS2 Controller Class
int error = 0; 
byte type = 0;
byte vibrate = 0;
unsigned long remoteTimer = 0;

void setup() 
{
  __setup_serial__();
  __setup_remote__();
  __setup_stepping__();
  __setup_digital__();
}

void loop() 
{
  __ctrl_serial__();
  __ctrl_remote__();
  __ctrl_stepping__();
  __ctrl_digital__();

}
