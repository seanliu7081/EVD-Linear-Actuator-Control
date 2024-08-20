#include <AccelStepper.h>

#define stepPin 5
#define dirPin 8
#define motorInterfaceType 1

// Encoder pins
#define encoderPinA 2
#define encoderPinB 3

volatile long encoderCount = 0;
int lastEncoded = 0;
long lastEncoderCount = 0;
unsigned long lastCheckTime = 0;

AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

void setup() {
  Serial.begin(115200);
  pinMode(encoderPinA, INPUT_PULLUP);
  pinMode(encoderPinB, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(encoderPinA), updateEncoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderPinB), updateEncoder, CHANGE);

  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(500);
}

void loop() {
  if (Serial.available() > 0) {
    float distance = Serial.parseFloat();  // Read the incoming distance
    moveMotor(distance);
    Serial.println("Done");  // Send confirmation back to Python
  }
  // stepper.run();
}

void moveMotor(float cm) {
  long targetSteps = cm * 200;
  stepper.move(targetSteps);  // Queue the movement
  while (stepper.distanceToGo() != 0) {
    stepper.run();  // Continuously run the stepper motor until the target is reached
  }
}

void updateEncoder() {
  int MSB = digitalRead(encoderPinA);
  int LSB = digitalRead(encoderPinB);
  int encoded = (MSB << 1) | LSB;
  int sum = (lastEncoded << 2) | encoded;

  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderCount++;
  if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderCount--;
  lastEncoded = encoded;
}
