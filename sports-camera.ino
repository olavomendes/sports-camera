const int BUTTON = 2;
bool lastState = LOW;
unsigned long lastPress = 0;

void setup() {
  pinMode(BUTTON, INPUT);
  Serial.begin(9600);
  Serial.println("Arduino pronto");
}

void loop() {
  bool state = digitalRead(BUTTON);
  if (state == HIGH && lastState == LOW
      && millis() - lastPress > 200) {
    Serial.println("SALVAR");
    lastPress = millis();
  }
  lastState = state;
  delay(10);
}