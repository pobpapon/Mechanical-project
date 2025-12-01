
void __setup_digital__()
{
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(LOCK_PIN, OUTPUT);
}

void __ctrl_digital__()
{
  digitalWrite(TRIGGER_PIN, triggerState);
  digitalWrite(LOCK_PIN, pitchLock);
}

