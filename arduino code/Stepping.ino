void __setup_stepping__() 
{
  for(uint8_t i=0; i<2; i++)
  {
    pinMode(ENA_PIN[i], OUTPUT);
    pinMode(PUL_PIN[i], OUTPUT);
    pinMode(DIR_PIN[i], OUTPUT);
    digitalWrite(ENA_PIN[i], 0);
    digitalWrite(PUL_PIN[i], 0);
    digitalWrite(DIR_PIN[i], 0);
  }
}

void __ctrl_stepping__()
{
  for(uint8_t i=0; i<2; i++) 
  {
    if(StepSpd[i] != 0)
    {
      int8_t stepDir = SIGN(StepSpd[i]);
      //digitalWrite(ENA_PIN[i], 0);
      digitalWrite(DIR_PIN[i], stepDir > 0 ? 1 : 0);
      unsigned long stepDelay = map(abs(StepSpd[i]), 1, 10000, MAX_STEP_DELAY, MIN_STEP_DELAY);

      if(micros() - StepTimer[i] >= stepDelay)
      {
        digitalWrite(PUL_PIN[i], StepState[i]);
        if(StepState[i])
        {
          StepCnt[i] += stepDir;     
        }
        StepState[i] =! StepState[i];
        StepTimer[i] = micros();
      }
    }
    else
    {
      StepState[i] = 0;
      //digitalWrite(ENA_PIN[i], 1);
      digitalWrite(PUL_PIN[i], StepState[i]);
      StepTimer[i] = micros();
    }
  }  
}
