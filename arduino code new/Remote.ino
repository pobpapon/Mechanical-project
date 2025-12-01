void __setup_remote__()
{
 //CHANGES for v1.6 HERE!!! **************PAY ATTENTION*************
  
 error = ps2x.config_gamepad(13,11,10,12, true, true);   
 //setup pins and settings:  GamePad(clock, command, attention, data, Pressures?, Rumble?) check for error  

 switch(error)
 {
   case 0: Serial.println("Found Controller, configured successful");           break;
   case 1: Serial.println("No controller found, check wiring.");                break;
   case 2: Serial.println("Controller found but not accepting commands.");      break;
   case 3: 
    Serial.println("Controller refusing to enter Pressures mode, may not support it.");    
    type = ps2x.readType(); 
    switch(type) 
    {
      case 0: Serial.println("Unknown Controller type");      break;
      case 1: Serial.println("DualShock Controller Found");   break;
      case 2: Serial.println("GuitarHero Controller Found");  break;
    }     
  break;
 }
}

void __ctrl_remote__()
{
  if(error == 1) { return; }  

  if(type == 1)
  {
    if(millis() - remoteTimer >= 50)
    {
      ps2x.read_gamepad(false, vibrate);  //read controller and set large motor to spin at 'vibrate' speed

      triggerState = ps2x.Button(PSB_BLUE);
      vibrate = triggerState*255;

      int remoteAnalog = ps2x.Analog(PSS_LY);
      //Serial.println(remoteAnalog);
      if(remoteAnalog > 133)
      {
        StepSpd[1] = map(remoteAnalog, 181, 255, 1, 10000); 
      }
      else if(remoteAnalog < 123)
      {
        StepSpd[1] = map(remoteAnalog, 179, 0, -1, -10000);
      }
      else
      {
        StepSpd[1] = 0;  
      }

      if(ps2x.ButtonPressed(PSB_RED))
      {
        pitchLock = true;
      }
      else if(ps2x.ButtonPressed(PSB_PINK))
      {
        pitchLock = false; 
      }

      remoteAnalog = ps2x.Analog(PSS_RX);
      //Serial.println(remoteAnalog);
      if(remoteAnalog > 133)
      {
        StepSpd[0] = map(remoteAnalog, 181, 255, 1, 10000); 
      }
      else if(remoteAnalog < 123)
      {
        StepSpd[0] = map(remoteAnalog, 179, 0, -1, -10000);
      }
      else
      {
        StepSpd[0] = 0;  
      }



      //Serial.print(StepSpd[0]);   Serial.print("\t");   Serial.println(StepSpd[1]);

      remoteTimer = millis();
    }
  }
}
