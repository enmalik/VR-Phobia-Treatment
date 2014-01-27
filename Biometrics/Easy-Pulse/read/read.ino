int pulsePin = 0;// Pulse Sensor purple wire connected to analog pin 0
// int msTime = 0;
int delayTime = 40; // ms delay

unsigned long msTime = 0;

void setup() {
	Serial.begin(115200);
}

void loop() {
        msTime += delayTime;
	int sensorValue = analogRead(pulsePin);
        Serial.print(msTime);
        Serial.print(' ');
	Serial.println(sensorValue);
	delay(delayTime);

//  int sensorValue = analogRead(pulsePin);
//  Serial.println(sensorValue);
//  delay(delayTime);
}
