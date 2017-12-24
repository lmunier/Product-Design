//*******************************************************************//
//smarbin.ino
//
// Last revision : 21.12.17
//Authors : Simone Sanso & Louis Munier
//*******************************************************************//

#include "Particle.h"
#include <SPI.h>
#include "epd2in9.h"
#include "epdpaint.h"
#include <string.h>

#define COLORED     0
#define UNCOLORED   1

unsigned char image[1024];
Paint paint(image, 0, 0, ROTATE_0);    // width should be the multiple of 8
Epd epd;
unsigned long time_start_ms;
unsigned long time_now_s;

// Function prototypes

// Constantes defines for TCP connexion
IPAddress serverAddr = IPAddress(192, 168, 43, 176);
int serverPort = 2048;

TCPClient client;

// PIN definitions
int ultrasonic_TRIG = A0;       //ultrasonic wave sent out
int ultrasonic_ECHO = A1;       //ultrasonic wave received in
int wake_up_switch  = D1;       //switch goes to 1 when the doors close

// Variable defines to compute distance
float speed = 330.0;            //m/s
long duration_us = 0;
float duration = 0.0;           //s
float distance_cm = 0;
float max_distance = 22;
float min_distance = 13.8;

int full_percent = 100;
int offset_percent = 50;
bool measure = true;

// Variables to send
char id_bin_val[] = "CO1_M1";
int filling_val = 0;
int battery_val = 75;

// Variable to do finite state and save power
int address_save_int = 0;
int save_power = 2;

int address_save_fil = 1;

// Functions prototypes
float measure_distance();
void sendData(char[], int, int);
void init_text();
void filling_update(int);
void battery_update(int);

//--------------------------------
// For DEMO
int wait_before_measure = 5000;
int wait_before_deepsleep = 5;
//--------------------------------

void setup() {
  Serial.begin(9600);

  // Initialize each pin
  pinMode(ultrasonic_TRIG, OUTPUT);
  pinMode(ultrasonic_ECHO, INPUT);
  pinMode(wake_up_switch, INPUT_PULLUP);    //pin active-low

  // Check if it's the first run and implement int save_power
  // We save it on EEPROM to keep it after deep sleep mode and initiaiate screen
  if(EEPROM.read(address_save_int) == 0xff){
      save_power = 0;
      EEPROM.write(address_save_int, save_power);
  }


  // Setup spi connection
  if (epd.Init(lut_particle_update) != 0) {
      // To debug, message if failed
      //Serial.print("e-Paper init failed");
      return;
  }

  epd.ClearFrameMemory(0xFF);   // bit set = white, bit reset = black
  epd.DisplayFrame();
  epd.ClearFrameMemory(0xFF);   // bit set = white, bit reset = black
  epd.DisplayFrame();

  init_text();
  battery_update(75);

  filling_update(EEPROM.read(address_save_fil));

  /**
   *  there are 2 memory areas embedded in the e-paper display
   *  and once the display is refreshed, the memory area will be auto-toggled,
   *  i.e. the next action of SetFrameMemory will set the other memory area
   *  therefore you have to clear the frame memory twice.
   */
}

void loop() {
    save_power = EEPROM.read(address_save_int);

    if(save_power == 0){
        // Toggle save_power and save it
        save_power = 1;
        EEPROM.write(address_save_int, save_power);

        filling_update(filling_val);
        battery_update(80);

        // Send chip to deep sleep mode
        System.sleep(SLEEP_MODE_DEEP, wait_before_deepsleep);
    }
    else{
        // Toggle save_power and save it
        save_power = 0;
        EEPROM.write(address_save_int, save_power);

        // Send the chip to sleep mode
        System.sleep(wake_up_switch, RISING);

        // Interruption
        delay(wait_before_measure);

        while(measure){
          if (digitalRead(wake_up_switch))
            measure = false;
        }

        delay(wait_before_measure);

        // Do the measurement, send value to database on server
        filling_val = offset_percent+
                    (full_percent-offset_percent)*(max_distance-measure_distance())/(max_distance-min_distance);
        sendData(id_bin_val, filling_val, battery_val);

        EEPROM.write(address_save_fil, filling_val);
        filling_update(filling_val);
        battery_update(80);
    }
}

//Determine the current distance
float measure_distance(){
    //pulse generation (works for both digital and analog pins)
    digitalWrite(ultrasonic_TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(ultrasonic_TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(ultrasonic_TRIG, LOW);

    // Computing the distance
    duration_us = pulseIn(ultrasonic_ECHO, HIGH);   //microseconds
    duration = duration_us / 1000000.0;             //seconds
    distance_cm = (duration * 0.5) * speed *100.0;  //cm

    if (distance_cm >= 200 || distance_cm <= 0){
        distance_cm = measure_distance();
    }

    return distance_cm;
}

void sendData(char id_bin[], int filling, int battery) {
    if (!client.connected()) {
		client.connect(serverAddr, serverPort);
	}

	if (client.connected()) {
		char data_to_send[256];

		// Prepare a buffer with data_to_send
		snprintf(data_to_send, sizeof(data_to_send), "id_bin %s, filling %d, battery %d", id_bin, filling, battery);

		// Send to the server. Send only a LF line terminator because it makes parsing easier
		// on the node.js side
		client.printf("%s", data_to_send);
	}

	if(client.read() == 'y')
	    client.stop();
}

void init_text(){
  // Write "Welcome to the futur"
  paint.SetHeight(160);
  paint.SetWidth(16);
  paint.SetRotate(ROTATE_90);

  paint.Clear(UNCOLORED);
  paint.DrawStringAt(0, 0, "Welcome to the", &Font16, COLORED);
  epd.SetFrameMemory(paint.GetImage(), 64, 52, paint.GetWidth(), paint.GetHeight());

  paint.SetHeight(110);
  paint.SetWidth(24);

  paint.Clear(COLORED);
  paint.DrawStringAt(4, 2, "Future", &Font24, UNCOLORED);
  epd.SetFrameMemory(paint.GetImage(), 32, 94, paint.GetWidth(), paint.GetHeight());

  // Write "Team members"
  paint.SetHeight(220);
  paint.SetWidth(8);

  paint.Clear(UNCOLORED);
  paint.DrawStringAt(0, 0, "Chaoui Aziz ,Dias, Munier, Sanso & Schenker", &Font8, COLORED);
  epd.SetFrameMemory(paint.GetImage(), 0, 70, paint.GetWidth(), paint.GetHeight());

  // Write "SmartBin.zip"
  paint.SetHeight(220);
  paint.SetWidth(24);

  paint.Clear(UNCOLORED);
  paint.DrawStringAt(0, 0, "SmartBin.zip", &Font24, COLORED);
  epd.SetFrameMemory(paint.GetImage(), 90, 50, paint.GetWidth(), paint.GetHeight());
  epd.DisplayFrame();

  delay(1000);
}

void filling_update(int fil){
  // Variable for bin logo
  char filling[5];
  int y_min = 0, y_max = 0;
  int x_bin[] = {0, 64, 64, 0};
  int y_bin[] = {0, 15, 43, 57};
  int len_bin = sizeof(x_bin)/sizeof(int);
  int full = 100;

  // Draw bin logo
  paint.SetWidth(64);
  paint.SetHeight(57);
  paint.SetRotate(ROTATE_180);

  paint.Clear(UNCOLORED);

  int point=0;
  for(point=0; point<1; point++){
    paint.DrawLine(x_bin[point], y_bin[point], x_bin[point+1]+3, y_bin[point+1], COLORED);
    paint.DrawLine(x_bin[len_bin-point-1], y_bin[len_bin-point-1],
                   x_bin[len_bin-point-2]+3, y_bin[len_bin-point-2]-2, COLORED);
  }
  paint.DrawVerticalLine(x_bin[point], y_bin[point], y_bin[point+1]-y_bin[point]+1, COLORED);
  paint.DrawVerticalLine(x_bin[point]-1, y_bin[point], y_bin[point+1]-y_bin[point]+1, COLORED);

  for(int x_var=fil*(x_bin[1]-x_bin[0])/100; x_var>0; x_var--){
    y_min = y_bin[1]-16*x_var/64;
    y_max = y_bin[2]+14*x_var/64;

    paint.DrawVerticalLine(x_bin[1]-x_var, y_min, y_max-y_min, COLORED);
  }

  epd.SetFrameMemory(paint.GetImage(), 8, 4, paint.GetWidth(), paint.GetHeight());
  epd.DisplayFrame();
  epd.SetFrameMemory(paint.GetImage(), 8, 4, paint.GetWidth(), paint.GetHeight());
  epd.DisplayFrame();

  delay(1000);
}

void battery_update(int bat){
  // Variables for battery logo
  int x_bat[] = {8, 12, 12, 112, 112, 12, 12, 8};
  int y_bat[] = {12, 12, 8, 8, 24, 24, 20, 20};
  int len_bat = sizeof(x_bat)/sizeof(int);
  int full = 100;

  // Battery update
  paint.SetWidth(113);
  paint.SetHeight(25);
  paint.SetRotate(ROTATE_180);

  paint.Clear(UNCOLORED);
  paint.DrawHorizontalLine(x_bat[0], y_bat[0], x_bat[1]+1-x_bat[0], COLORED);
  paint.DrawVerticalLine(  x_bat[2], y_bat[2], y_bat[1]-y_bat[2],   COLORED);
  paint.DrawHorizontalLine(x_bat[2], y_bat[2], x_bat[3]-x_bat[2],   COLORED);
  paint.DrawVerticalLine(  x_bat[3], y_bat[3], y_bat[4]-y_bat[3],   COLORED);
  paint.DrawHorizontalLine(x_bat[5], y_bat[5], x_bat[4]-x_bat[5],   COLORED);
  paint.DrawVerticalLine(  x_bat[6], y_bat[6], y_bat[5]-y_bat[6],   COLORED);
  paint.DrawHorizontalLine(x_bat[7], y_bat[7], x_bat[6]-x_bat[7],   COLORED);
  paint.DrawVerticalLine(  x_bat[0], y_bat[0], y_bat[7]-y_bat[0],   COLORED);

  if(bat > 95){
    paint.DrawFilledRectangle(x_bat[0], y_bat[0], x_bat[6], y_bat[6], COLORED);
    paint.DrawFilledRectangle(x_bat[2], y_bat[2], x_bat[4], y_bat[4], COLORED);
  }
  else
    paint.DrawFilledRectangle(x_bat[2]+(full-bat)*(x_bat[4]-x_bat[2])/100,
                              y_bat[2], x_bat[4], y_bat[4], COLORED);

  epd.SetFrameMemory(paint.GetImage(), 8, 272, paint.GetWidth(), paint.GetHeight());
  epd.DisplayFrame();
  epd.SetFrameMemory(paint.GetImage(), 8, 272, paint.GetWidth(), paint.GetHeight());
  epd.DisplayFrame();

  delay(1000);
}
