int red = 12;   // Red LED pin
int green = 13; // Green LED pin
const unsigned long greenmaxlimit = 100000; // Maximum green light duration
const unsigned long redmaxlimit = 80000;   // Maximum red light duration

void setup() {
  Serial.begin(9600);  
  pinMode(red, OUTPUT);  
  pinMode(green, OUTPUT);  
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    int commaIndex = input.indexOf(',');

    if (commaIndex != -1) {
      String value1 = input.substring(0, commaIndex);
      String value2 = input.substring(commaIndex + 1);

      int peopleCount = value1.toInt();  
      int vehicleCount = value2.toInt();  

      // Conditions for different scenarios
      if (peopleCount >= 10 && vehicleCount <= 4) {   // Crowd
        digitalWrite(red, HIGH);
        delay(40000);
        digitalWrite(red, LOW);
      } 
      else if (peopleCount <= 4 && vehicleCount >= 7) {  // Traffic
        digitalWrite(green, HIGH);
        delay(100000);
        digitalWrite(green, LOW);
      } 
      else if (peopleCount >= 20 && vehicleCount >= 4) {  // Peak Crowd
        digitalWrite(red, HIGH);
        if (peopleCount == 0) {
          digitalWrite(red, LOW);
          return;
        }
        delay(80000);
        digitalWrite(red, LOW);
      } 
      else if (peopleCount <= 4 && vehicleCount >= 12) {  // Peak Traffic
        digitalWrite(green, HIGH);
        unsigned long chck_clear = millis();
        while (millis() - chck_clear < greenmaxlimit) {
          if (vehicleCount <= 4) {
            digitalWrite(green, LOW);
          }
        }
        digitalWrite(green, LOW);
      } 
      else if (peopleCount >= 15 && vehicleCount >= 8) {  // Extended Crowd
        digitalWrite(red, HIGH);
        unsigned long crowd_chck = millis();
        while (millis() - crowd_chck < redmaxlimit) {
          if (peopleCount <= 3) {
            digitalWrite(red, LOW);
          }
        }
        digitalWrite(red, LOW);
      } 
      else {
        // Default case
        int deflt = 0;
        while (deflt < 10) {
          if (peopleCount >= 3 && vehicleCount <= 3) {
            digitalWrite(red, HIGH);
            delay(30000);
            digitalWrite(red, LOW);
            delay(1000);
            digitalWrite(green, HIGH);
            delay(100000);
            digitalWrite(green, LOW);
          }
          deflt = 26;
        }
      }
    }
  }
  delay(1000); // Delay for the next loop iteration
}
