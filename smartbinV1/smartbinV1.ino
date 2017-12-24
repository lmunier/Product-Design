//*******************************************************************//
//smarbin.ino
//
// Last revision : 18.12.17
//Authors : Simone Sanso & Louis Munier
//*******************************************************************//

int ultrasonic_TRIG = A0;   //ultrasonic wave sent out
int ultrasonic_ECHO = A1;   //ultrasonic wave received in
int wake_up_switch  = D0;   //switch goes to 1 when the doors close

unsigned int count = 0;     //number of measurements (from 0 to 9)
unsigned int mean_count = 0;//number of mean_distance_cm given

float speed = 330.0;          //m/s
long duration_us = 0;
float duration = 0.0;       //s
float distance_cm = 0;
//float distance_cm [10];    //cm, index of the array goes from 0 to 9
//float mean_distance_cm = 0.0;


void setup() {
    Serial.begin(9600);

    pinMode(ultrasonic_TRIG, OUTPUT);
    pinMode(ultrasonic_ECHO, INPUT);
    pinMode(wake_up_switch, INPUT_PULLUP);    //pin active-low

    /*for (int i = 0; i < 10; i++) {
        distance_cm [i] = 0.0;
    }*/

}

//Determine the current distance
float measure_distance(){
    //pulse generation (works for both digital and analog pins)
    digitalWrite(ultrasonic_TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(ultrasonic_TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(ultrasonic_TRIG, LOW);

    // Measurement of the distance
    duration_us = pulseIn(ultrasonic_ECHO, HIGH);  //microseconds
    duration = duration_us / 1000000.0;  //seconds
    distance_cm = (duration * 0.5) * speed *100.0; //cm

    if (distance_cm >= 200 || distance_cm <= 0){
        distance_cm = measure_distance();
    }
    else {
        //Serial.print("MEASURE "); Serial.print(count); Serial.println("");
        Serial.print(distance_cm);
        Serial.println(" cm"); Serial.println("");
        // Serial.print(duration_us, 9);
        // Serial.println(" us"); Serial.println("");
    }

    return distance_cm;
}

//Determines the average of the past 10 measurements
/*void calculate_mean_distance(){
    for (int i = 0; i < 10; i++) {
        mean_distance_cm += distance_cm[i];
    }
    mean_distance_cm = mean_distance_cm / 10.0;

    Serial.print("AVERAGE_DISTANCE"); Serial.print(mean_count);
    Serial.print("= "); Serial.println(mean_distance_cm);
}*/

// Turn off Wi-Fi. Pause microcontroller.
// Application resumes on pin trigger or after seconds.
// Very low power usage.
void send_to_sleep_mode(){
    Serial.println("SLEEP_MODE activated for 90 seconds");
    Serial.println("Wake me up by using the trash !");
    // System.sleep(wakeUpPin, edgeTriggerMode, seconds);
    System.sleep(wake_up_switch, RISING, 90);
}

//Initiated after the Photon wakes up.
//Initializes all the functions of the Photon for it to work.
// void photonWakeUp(){
//     printTimer = millis();        //giving a value to the printTimer
//     digitalWrite(statePin, HIGH); //Turning the distance sensor on.
//     WiFi.on();                    //Turning WiFi on...
//     WiFi.connect();               //Making it connect...
//
//     //Getting previously stored values from the EEPROM.
//     //Used to check if there's still data from previous session.
//     EEPROM.get(eepromAddress[0], eepromValue1);
//     EEPROM.get(eepromAddress[1], eepromValue2);
//
//     //Checking if it's connected, to...
//     if(Particle.connected()){
//       delay(cooldown);
//       detectTime();               //detect time
//       firstRun = false;           //and to exit the firstRun.
//     }
//     else{
//       photonWakeUp();
//     }
// }

void loop() {
    //This is executed when Photon turns on (this includes after a deep sleep)
    // while(firstRun == true){
    //     photonWakeUp();
    // }

    Serial.println(measure_distance());
    delay(500);
    /*if (count = 10) {
        count = 0;
        calculate_mean_distance();
        //send_to_sleep_mode();
    }*/
}

