#include <iostream>
#include <Wire.h>
#include <arduinoFFT.h>
#include "SPIFFS.h" 
#include <LiquidCrystal.h>
#include <ArduinoJson.h>
// for next time spiffs to log data


#define accel_module (0x53)
#define xyzregister (0x32)
#define SAMPLES 256              // Must be power of 2
#define SAMPLING_FREQ 256     // Hz

#define accel_module (0x53)
#define dataPin4 14
#define dataPin5 27
#define dataPin6 26 
#define dataPin7 25
#define rs 13
#define en 12
#define buttonInputPin 34
#define SamplingLength 46336 // 46080 + 256 to guard against auto time errors/ lags
#define TimeStore 180



uint8_t FreqCounter = 0;
int16_t SampleData[SamplingLength] = {};
unsigned long AssociatedTimesSData[SamplingLength] = {};
unsigned long AssociatedTimesFreqData[TimeStore] = {};
uint8_t AssociatedFrequencies[TimeStore] = {}; // updates every second for 180 seconds
uint8_t button_state = 0;
bool process = false;
bool checking = false;
bool waitingForRelease = false;
bool printed = false;
uint16_t counterData = 0;

ArduinoFFT<double> FFT = ArduinoFFT<double>();
LiquidCrystal lcd(rs, en, dataPin4, dataPin5, dataPin6, dataPin7); 

double vReal[SAMPLES], vImag[SAMPLES];



byte values[6]; //# array of 6 bytes

//int16_t ListValues[Window_Size];
float averageVal;
static bool calibrated = false;
static int16_t offsetX = 0, offsetY = 0, offsetZ = 0;
int16_t Samples[SAMPLES];
float frequency;
int16_t filterVal = 0;
const float alpha = 0.1f; 
uint16_t counter = 0;
unsigned long currentTime = 0;
unsigned long previousTime = 0;
uint8_t maxIndex = 0;
double maxVal;
unsigned long timeDelay;
char ToPrint[20];
int16_t x_raw,y_raw,z_raw;
float Xg_val, Yg_val, Zg_val;
unsigned long previousTimeButton = 0;
uint8_t cycles = 0;
bool ReadyToSave = false;











  






void setup() {
  // put your setup code here, to run once

  pinMode(buttonInputPin, INPUT);

  Wire.begin(21,22);
  Wire.setClock(400000); // lets do fast I2C to support the sampling Default is usually 100 KHZ
  lcd.begin(20, 4);
  Serial.begin(9600);

  Wire.beginTransmission(accel_module); // remember that accel_module is an address
  Wire.write(0x2D); //bite with value 45
  Wire.write(0); // clears register to 0 for new run 
  Wire.endTransmission();
  //tell arduino to write to this register 0X2D
   // set all bits to 0
  Wire.beginTransmission(accel_module);
  Wire.write(0x2D);
  Wire.write(16); // measure mode
  Wire.endTransmission();

  Wire.beginTransmission(accel_module);
  Wire.write(0x2D);
  Wire.write(8); // disable sleep mode 
  Wire.endTransmission();

  

  timeDelay = (1.0/SAMPLING_FREQ)*(1e6);
 /*
  if (!SPIFFS.begin(true)){
    Serial.println("Error: mounting SPIFFS");
    return; 
  }
  else{
    Serial.println("Mounting successful");
  }

  File file = SPIFFS.open("",FILE_WRITE);

  if(!file){
    Serial.println("Error: Opening File!");
    return;
  }


  if(file.print("... \n")){
    Serial.println("File was written");

  }

  else{
    Serial.println("File write failed");
  }
 


  //file.close();

  */ 
}








void applyIIR(int16_t NewVal) {
  filterVal = (alpha * NewVal) + ((1 - alpha) * (filterVal));
}

/*
void PopulateList(int16_t zVal){
  for(int i = 0; i < Window_Size; i++){
    if (ListValues[i] == 0){
      ListValues[i] = zVal;
      break;
    }
    populated++;
  }


}
*/ 
/*
typedef struct{
float b0, b1, b2; // feed forward mech
float a1, a2; //feed back mech
float w1, w2; // delayed states
} LPF2;
*/

void loop() {
  // put your main code here, to run repeatedly:

  if(ReadyToSave && !process){
      // this is the point where we pause the program and assemble everything for SPIFFS entry of json files
  // begin here:


  }

  else{

  button_state = digitalRead(buttonInputPin);
  
  
  if (button_state == 1 && !checking){ //begin for check for 3 seconds
    checking = true;
    previousTimeButton = millis();

  } 

  else if(button_state == 1 && checking){
    
    
    if(millis() - previousTimeButton >= 3000 && !waitingForRelease){
     
      // need to check if process is true to early trigger the end cycle by turning on Ready To Save
      process = !process; 
      cycles++;
      //checking = false;
      waitingForRelease = true;
      printed = false;
      
      
    }

  

  }
  else if(button_state == 0 && checking == true){
    checking = false;
    waitingForRelease = false;
  }


  


 

  //INEFFICIENT
   // int xyzregister = 0x32; // where first register is: DATAX0 from datasheet
    //int16_t x_raw,y_raw,z_raw;
    //float Xg_val, Yg_val, Zg_val;

    Wire.beginTransmission(accel_module);
    Wire.write(xyzregister); // send value 50
    Wire.endTransmission();

    Wire.beginTransmission(accel_module);
    Wire.requestFrom(accel_module, 6); // wait for response of 6 bytes

    int i = 0;  

    while(Wire.available()){ // non zero value is treated as a true conditional (just a shortcut to Wire.available() != 0)
      values[i] = Wire.read(); // read each of the 6 bytes 1 by 1 and push them into the value array
      i++;
    }

    Wire.endTransmission();

    x_raw = (int16_t)((values[1] << 8) | values[0]);  //cast as 16 bit int, and then or it with the binary of the byte of values[0], to get byte 1 and byte 2 to make up an int (this actually works differently for an esp32)
    y_raw = (int16_t)((values[3] << 8) | values[2]); // correction to above comment, cast actually happens last.
    z_raw = (int16_t)((values[5] << 8) | values[4]); // This is because operations happen in 32 bit


// MUST NOT TOUCH SENSOR FOR 5 seconds
    if (!calibrated && millis() > 5000) { // if we are not calibrated and the time is greaater than 5 seconds, then:
    offsetX = x_raw;
    offsetY = y_raw;
    offsetZ = z_raw;   // Sccubtract 1g from Z
    calibrated = true;
  }

  
  if (calibrated) {
    x_raw -= offsetX;
    y_raw -= offsetY;
    z_raw -= offsetZ;
  }

  /*if(calibrated) {
    for (int i = 0; i < SAMPLES; i++) {
    vReal[i] = z_raw;         // Raw or filtered
    vImag[i] = 0;
    delayMicroseconds(1000000 / SAMPLING_FREQ); // in one second, I want 1000 data points
    // how much do I have to delay in a second to do that? x * 1000 = 1 * 10^6 (this is all in microsecondsthis
    //Fill up with a data point every 1000000 / SAMPLING_FREQ microseconds or 10^3 microseconds which is 0.001 seconds
  }
  }
  */

  //
  /**/

  /*
  if(calibrated){
  FFT.windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.compute(vReal, vImag, SAMPLES, FFT_FORWARD);
  FFT.complexToMagnitude(vReal, vImag, SAMPLES);

  double peak = 0;
  int peak_idx = 0;
  for (int i = 1; i < (SAMPLES/2); i++) {
    if (vReal[i] > peak) {
      peak = vReal[i];
      peak_idx = i;
    }
  }

  frequency = peak_idx * (SAMPLING_FREQ / SAMPLES);

  }
  */
  





  /*if(){
    PopulateList(z_raw);
  }
  */ 



    /*Xg_val = (x_raw / 256.0f);
    Yg_val = (y_raw / 256.0f);
    Zg_val = (z_raw / 256.0f);
    */

    //ask mohanty whether we should be doing these averages with the LSBs or the g values (for efficiency, we probably just want the LSB's to be handled)

    //zfilteredValue = alpha * Zg_val + (1 - alpha) * zfilteredValue; // filtered val is 10 percent of the Zg_val and 90% of the pastval


    // receiving frequency 
    
    

    //sprintf(output, "g-vals: %f %f %f \n tilt-vals: %f %f %f", Xg_val, Yg_val, Zg_val); // store data into char arary
    /*if(calibrated){
    Serial.printf("Freq: %.2f Hz (Peak: %.0f) \n", frequency, peak) // Serial print that char array
    Serial.write(10); // send raw ASCII character of new line to go to the next line.
    }
*/  //Serial.println(z_raw);
    applyIIR(z_raw);
    Serial.println(filterVal);
    currentTime = micros();
    if(calibrated && counter < 256 && currentTime - previousTime >= timeDelay){
      Samples[counter] = filterVal;
      if (process && counterData < SamplingLength){
        SampleData[counterData] = filterVal;
        AssociatedTimesSData[counterData] = micros();
        counterData++;
      }
      
      counter++;
      previousTime = currentTime;

    }
    
    else if (calibrated && counter == 256){
      //counter = 0;
      for (int i = 0; i < SAMPLES; i++) {
      vReal[i] = (double)Samples[i];   // Your ADC samples
      vImag[i] = (double)0;    
      }       // Must be zero!

      FFT.windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
      FFT.compute(vReal, vImag, SAMPLES, FFT_FORWARD);
      FFT.complexToMagnitude(vReal, vImag, SAMPLES);
      // on towards finding the maximum frequency
      maxIndex = 0;
      maxVal = vReal[0];
      for (int i = 1; i < 256; i++){
        
        if (vReal[i] > maxVal){
          maxIndex = i;
          maxVal = vReal[i];
        }

      

      
      }

      
//future note, let's optimize calculations for more bin widths instead so that we can more accurate readings. Close to 1 second is okay. Supposing that we stay at 512, we can reduce the sampling frequency --> therefore increasing the period to collect all 256 samples.
      lcd.setCursor(1, 1);
      sprintf(ToPrint, "freq: %d hz   ", maxIndex);

      //Serial.println(ToPrint);
      lcd.print(ToPrint);
      sprintf(ToPrint, "Time: %d (s) ", (int)(currentTime/(1000000UL)));
      lcd.setCursor(0,3); // col row
      lcd.print(ToPrint);
      if (process && !printed){
        lcd.setCursor(0,4);
        sprintf(ToPrint, "Saving Data    ")
        lcd.print(ToPrint)
        printed = !printed;
      }
      else if(!process && !printed)
        lcd.setCursor(0,4);
        sprintf(ToPrint, "Not Saving Data")
        lcd.print(ToPrint)
        printed = !printed;

        if (process && FreqCounter < 180){
        AssociatedFrequencies[FreqCounter] = maxIndex;
        AssociatedTimesSData[FreqCounter] = micros();
        FreqCounter++;

        // unsigned long AssociatedTimesFreqData[TimeStore] = {};
        //uint8_t AssociatedFrequencies[TimeStore] = {}; FreqCounter
      }
      elif(FreqCounter == TimeStore){ // auto stop, may need to move this to the filtered value storage

        // At this point we save the list through spiffs
        process = !process;
        printed = false;
        ReadyToSave = true;


      }
    
      }

      counter = 0;
      //expect a return every second given how we organized the values

// bin step = fs(sampling freq) / Num samples

  }
      
  }

  


    
// 



 



