const int frontPin = 4;   //Yellow (Yellow)
const int  backPin = 5;   //Brown  (Green?)
const int  leftPin = 2;   //Blue   (Green?)
const int rightPin = 3;   //Orange (Yellow)
int input;

void setLow(){
    digitalWrite(frontPin, LOW);
    digitalWrite(backPin, LOW);
    digitalWrite(leftPin, LOW);
    digitalWrite(rightPin, LOW);
}

void setup() {
    input = 'f';
    setLow();
    Serial.begin(9600);
}

// w - forward            s - back
// a - left               d - right
// q - stop acceleration  e - stop turning
// f - stop all motors

// Each function only deals with its its counterpart leaving the other half constant
// Forward only disables reverse but leaves left/right untouched
// Left only disables right but leaves front/back as is

// 'q' and 'e' work well since they stop linear / angular motion entirely.
// 'q' need not know if the car was moving forward or back, it simply stops both.
// Similarly pressing 'e' stops the car turning, regardless if the car was going left or right.

void loop() {
    if(Serial.available() > 0){
        //input = Serial.readStringUntil('\n');
        input = Serial.read();
        if(input == 'w'){
            digitalWrite(backPin,  LOW);
            digitalWrite(frontPin, HIGH);
            //Serial.println("Set to Forward");
        }
        else if(input == 's'){
            digitalWrite(frontPin, LOW);
            digitalWrite(backPin,  HIGH);
            //Serial.println("Set to Back");
        }
        else if(input == 'a'){
            digitalWrite(rightPin, LOW);
            digitalWrite(leftPin,  HIGH);
            //Serial.println("Set to Left");
        }
        else if(input == 'd'){
            digitalWrite(leftPin,  LOW);
            digitalWrite(rightPin, HIGH);
            //Serial.println("Set to Right");
        }
        else if(input == 'q'){
            digitalWrite(frontPin, LOW);
            digitalWrite(backPin,  LOW);
            //Serial.println("Stopped Accelerating");
        }
        else if(input == 'e'){
            digitalWrite(leftPin,  LOW);
            digitalWrite(rightPin, LOW);
            //Serial.println("Stopped Turning");
        }
        else if(input == 'f'){
            setLow();
            //Serial.println("Stopped All");
        }
    }
}
