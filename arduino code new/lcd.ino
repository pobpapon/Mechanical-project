#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

float currentPitch = 0.0;
float currentYaw = 0.0;

void __setup__lcd() {
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Pitch: 0.00");
  lcd.setCursor(0, 1);
  lcd.print("Yaw:   0.00");
}

void __update__lcd() {
  lcd.setCursor(7, 0);
  lcd.print("       ");
  lcd.setCursor(7, 0);
  lcd.print(currentPitch, 2);

  lcd.setCursor(7, 1);
  lcd.print("       ");
  lcd.setCursor(7, 1);
  lcd.print(currentYaw, 2);
}
