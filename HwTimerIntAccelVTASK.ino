#include <iostream>
#include <Wire.h>
#include <arduinoFFT.h>
#include <LiquidCrystal.h>
#include <cstdio>


#define accel_module (0x53)
#define xyzregister (0x32)
#define SAMPLES 2048              // Must be power of 2 // SAMPLES * 1/freq (s) every 1/500 seconds I take a data point, and store it: = 4.096 
#define SAMPLING_FREQ 500     // Hz receommended by Grok

#define configTICK_RATE_HZ 10000 // to make more precise sampling, but will move to hardware timerslong term

#define accel_module (0x53)
#define dataPin4 14
#define dataPin5 27
#define dataPin6 26 
#define dataPin7 25
#define rs 13
#define en 12
#define buttonInputPin 34
//#define SamplingLength 90000 // SAMPing freq * seconds for total used //          Deprecated lines because of RAM constraints: 20, 21, 27-30 inclusive, 36
//#define TimeStore 43

//typedef unsigned int ui; ui not needed: deprecated

volatile bool InitialHeaderPrint = false;
float CalculatedFreq = 0.0f;
//int16_t SampleData[SamplingLength] = {};
//unsigned long AssociatedTimesFreqData[TimeStore] = {};
//float AssociatedFrequencies[TimeStore] = {}; // updates every second for 180 seconds
uint8_t button_state = 0;
volatile bool process = false; // process starts out at false, so program won't run initially
volatile bool checking = false;
// bool not needed for now as long as button Read switches: bool waitingForRelease = false;
volatile bool printed = false;
//ui counterData = 0; Depcrecated
double bin_width = 500.0/2048;
volatile bool calculated = false;


ArduinoFFT<double> FFT = ArduinoFFT<double>();
double vReal[SAMPLES], vImag[SAMPLES];


LiquidCrystal lcd(rs, en, dataPin4, dataPin5, dataPin6, dataPin7); 

byte values[6]; // for accel Wire.available and read

volatile static bool calibrated = false;
static int16_t offsetX = 0, offsetY = 0, offsetZ = 0;


static int16_t Samples1[SAMPLES];
static int16_t Samples2[SAMPLES];
static unsigned long AssociatedTimesData1[SAMPLES];
static unsigned long AssociatedTimesData2[SAMPLES];
int16_t * ptr1 = &Samples1[0];
long unsigned int * ptr2 = &AssociatedTimesData1[0];
long unsigned int * serialptr2 = NULL;
int16_t * CalculatedPtr = NULL;
volatile bool switched = false;
volatile bool printed2 = false;
bool SerialPrinted = true;



int16_t filterVal = 0;
const float alpha = 0.1f; 
uint16_t counter = 0;
unsigned long currentTime = 0;
unsigned long previousTime = 0;
uint8_t maxIndex = 0;
double maxVal;
// deprecated - volatile float timeDelay; // may change to reg int num depending on result
char ToPrint[20];
int16_t x_raw,y_raw,z_raw;
unsigned long previousTimeButton = 0;
volatile bool ReadyToSave = false;

char CSVBuffer[30];
volatile int8_t Success; 

volatile bool buttonRead = true;

int i = 0; 

TaskHandle_t Sensing_task = NULL, Calculating_task = NULL, LCDPrinting_task = NULL, SerialPrinting_task = NULL;

//hardware timing because clearly we are not intervalling right:

hw_timer_t *timer = nullptr;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED; // Create Mutex
  
volatile bool sampleReady = false;


void applyIIR(int16_t NewVal) {
  filterVal = (alpha * NewVal) + ((1 - alpha) * (filterVal));
}

void IRAM_ATTR onTimer(){
  BaseType_t higherPriorityTaskWoken = pdFALSE; // essentially 0, and we check, upon freeRTOS trying to wake sensing from vTaskNotify, if ready to run, we store
  vTaskNotifyGiveFromISR(Sensing_task, &higherPriorityTaskWoken);
  portYIELD_FROM_ISR(higherPriorityTaskWoken); // if that higherpriority task woken is pdTrue, go time 

}




//why void * params? --> void foo(int *p) {
    //if (p != NULL) {
        // use *p
    //}
//} // Sensing will take params, but it will point to null later, so we are able to catch that when programming
void Sensing(void * parameters){

  //const TickType_t SensingDelay = pdMS_TO_TICKS(2);
  //TickType_t lastWakeTime = xTaskGetTickCount();
  
    for(;;){
    ulTaskNotifyTake(pdTRUE, portMAX_DELAY);// interact with Interrup service routine onTImer ( ) func
     // phenomenal because this task will take up 0 CPU, and allow watch dog to do IDLE tasks until it's time for the notify. It basically blocks the for, while telling watchdog you can continue.

    Wire.beginTransmission(accel_module);
    Wire.write(xyzregister); // send value 50
    Wire.endTransmission();

    Wire.beginTransmission(accel_module);
    Wire.requestFrom(accel_module, 6); // wait for response of 6 bytes

    while(Wire.available()){ // non zero value is treated as a true conditional (just a shortcut to Wire.available() != 0)
      values[i] = Wire.read(); // read each of the 6 bytes 1 by 1 and push them into the value array
      i++;
    }
    currentTime = micros();
    i = 0;

    Wire.endTransmission();

    x_raw = (int16_t)((values[1] << 8) | values[0]);  //cast as 16 bit int, and then or it with the binary of the byte of values[0], to get byte 1 and byte 2 to make up an int (this actually works differently for an esp32)
    y_raw = (int16_t)((values[3] << 8) | values[2]); // correction to above comment, cast actually happens last.
    z_raw = (int16_t)((values[5] << 8) | values[4]); // This is because operations happen in 32 bit



    if (!calibrated && millis() >= 5000) { // if we are not calibrated and the time is greaater than 5 seconds, then:
    offsetX = x_raw;
    offsetY = y_raw;
    offsetZ = z_raw;   // Sccubtract 1g from Z
    calibrated = true;
    }

    

    if (calibrated) {
    x_raw -= offsetX;
    y_raw -= offsetY;
    z_raw -= offsetZ;

    applyIIR(z_raw); 

    
    portENTER_CRITICAL(&timerMux);
    // deprecated - if(currentTime - previousTime >= timeDelay){
      // deprecated - previousTime = currentTime;
      if(counter == SAMPLES - 1){
        ptr1[counter] = filterVal; /*equivalent to *(ptr1 + index) = myVal by compiler*/
        ptr2[counter] = currentTime;
        counter = 0;
        if (ptr1 == &Samples1[0]){
            ptr1 = &Samples2[0];
            ptr2 = &AssociatedTimesData2[0];
        }
        else{
          ptr1 = &Samples1[0];
          ptr2 = &AssociatedTimesData1[0];
        }
        switched = true;
        calculated = false;
        

      }
      else{
      ptr1[counter] = filterVal;
      ptr2[counter] = currentTime;
      counter++;
      }
    //}
    portEXIT_CRITICAL(&timerMux); // let's use a mutex to ensure there's no weird access going on.
    }


    //vTaskDelayUntil(&lastWakeTime, SensingDelay);

    } // close for
} // close sensing

void Calculating(void * parameters){

  //const TickType_t CalcDelay = pdMS_TO_TICKS(2);
  //TickType_t lastWakeTimeCalc = xTaskGetTickCount();

  for(;;){
  
  if (calculated == false && switched == true){
  //portENTER_CRITICAL(*timerMux); // flip is usually atomic, but just in case, mutexing here could be valuable,
  if (ptr1 == &Samples1[0]){
    CalculatedPtr = &Samples2[0];
    serialptr2 = &AssociatedTimesData2[0];

  }
  else{
    CalculatedPtr = &Samples1[0];
    serialptr2 = &AssociatedTimesData1[0];
  }
  //portEXIT_CRITICAL(&timerMux);

  switched = false;

  

  for (int i = 0; i < SAMPLES; i++) {
        vReal[i] = (double)CalculatedPtr[i];   // Your ADC samples // equivalent to *ptr(i + index)
        vImag[i] = (double)0;
        } 

        FFT.windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
        FFT.compute(vReal, vImag, SAMPLES, FFT_FORWARD);
        FFT.complexToMagnitude(vReal, vImag, SAMPLES);

      maxIndex = 1; // we don't start at index 0, because that's DC bin
        maxVal = vReal[1];
        for (int i = 1; i <= SAMPLES/2; i++){ // for a freq of 500, we're looking at reliable and unique readings from index 0 to 250 since nyqiuist theorem exists   
        if (vReal[i] > maxVal){
          maxIndex = i; // NEED TO MULTIPLY MAX INDEX BY BIN WIDTH = fs / Num samples
          maxVal = vReal[i];
        }
      }
  CalculatedFreq = roundf((float(maxIndex * bin_width))*1000.0f) / 1000.0f;
  calculated = true; 
  printed2 = false;
  SerialPrinted = false;

  }

//vTaskDelayUntil(&lastWakeTimeCalc, CalcDelay);
  vTaskDelay(pdMS_TO_TICKS(1));
} // close infinite for
}

void LCDPrinting(void * parameters){

  //const TickType_t LCDDelay = pdMS_TO_TICKS(2);
  //TickType_t lastWakeTimeLCD = xTaskGetTickCount();

      for(;;){
      if (!calibrated && !printed){
        lcd.setCursor(0,3);
        sprintf(ToPrint, "Waiting...");
        lcd.print(ToPrint);
        lcd.setCursor(0,4);
        sprintf(ToPrint, "Not Calib.");
        lcd.print(ToPrint);
        printed = true;
      }

      if (printed && calibrated){ // food for thought later, we can make this it's own task and then delete it to pursue efficiency, keet that in mind
        lcd.clear();
        lcd.setCursor(0,4);
        sprintf(ToPrint, "Calib.");
        lcd.print(ToPrint);
        printed = false;

      }
      if (calculated && !printed2){
      
      sprintf(ToPrint, "fq: %.3f hz   ", CalculatedFreq); // precision up to 3 decimal points
      lcd.setCursor(0, 1);
      lcd.print(ToPrint);
      printed2 = true;
      }

      //Serial.println(ToPrint);
      
      // let's time base the below because we are interupting calcs this way
      sprintf(ToPrint, "Time: %d (s) ", (int)(currentTime/(1000000UL)));
      lcd.setCursor(0,3); // col row
      lcd.print(ToPrint);

      //vTaskDelayUntil(&lastWakeTimeLCD, LCDDelay);
      vTaskDelay(pdMS_TO_TICKS(5));
      }// close for
  
}

void SerialPrinting(void * parameters){
    //const TickType_t SerialDelay = pdMS_TO_TICKS(2);
    //TickType_t lastWakeTimeSerial = xTaskGetTickCount();
      // ReadyToSave will need to switch on once calibrated comes through // Extra note on this: there is no limit anymore, this just continuously goes
  // begin here: 
  for(;;){
  // easiest decision here is make a csv file and output it via serial
  if (InitialHeaderPrint == false){ // perhaps consider moving this chunk to a 1 move spot, but probably not necessary
  Success = snprintf(CSVBuffer, sizeof(CSVBuffer), "#Begin Data Trans\n");
  Serial.print(CSVBuffer);
  Success = snprintf(CSVBuffer,sizeof(CSVBuffer), "Time,SampleVal,Frq\n");
  Serial.print(CSVBuffer); 
  InitialHeaderPrint = true;
  }
  if (calibrated && calculated && !SerialPrinted){  // need to figure out this and below, and then we should be good. This is a good reason to understand mutexes and queue // althout keep in mind queue isn't good for long arrays/ better yet Task Notfies are better than mutexes, we shoudl implement both

    for(int k = 0; k < sizeof(Samples1)/sizeof(ptr1[0]); k++){
      Success = snprintf(CSVBuffer,sizeof(CSVBuffer), "%lu,%d,%.3f\n", serialptr2[k], CalculatedPtr[k], CalculatedFreq);
      Serial.print(CSVBuffer);
      }

  SerialPrinted = true;
  }

  

  //vTaskDelayUntil(&lastWakeTimeSerial, SerialDelay);
  vTaskDelay(pdMS_TO_TICKS(5));

  } // close for



}


void setup() {
  // put your setup code here, to run once:
  pinMode(buttonInputPin, INPUT);

  Wire.begin(21,22);
  Wire.setClock(400000); // lets do fast I2C to support the sampling Default is usually 100 KHZ
  lcd.begin(20, 4);
  Serial.begin(115200);
  delay(100);

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

  xTaskCreatePinnedToCore(
    Sensing,
    "Active_Accel_Sensing",
    5500, // might be wise to calculate stack size (in words)
    NULL, // 
    6, // highest prio as possible without getting rid of system tasks
    &Sensing_task, // pass in reference to TaskHandle_t
    1 //core 1 for important stuff
  );

  xTaskCreatePinnedToCore(
    SerialPrinting,
    "Serial_Printing",
    9000, // might be wise to calculate stack size (in words)
    NULL, // 
    4, // highest prio as possible without getting rid of system tasks
    &SerialPrinting_task, // pass in reference to TaskHandle_t
    0 //core 0 for less important stuff that will take time.
  );

  xTaskCreatePinnedToCore(
    LCDPrinting,
    "LCD_Printing",
    4000, // might be wise to calculate stack size (in words)
    NULL, // 
    4, // highest prio as possible without getting rid of system tasks
    &LCDPrinting_task, // pass in reference to TaskHandle_t
    0 //core 0 for less important stuff that will take time.
  );

  xTaskCreatePinnedToCore(
    Calculating,
    "Calcs",
    9000, // might be wise to calculate stack size (in words)
    NULL, // 
    5, // highest prio as possible without getting rid of system tasks
    &Calculating_task, // pass in reference to TaskHandle_t
    1 //core 0 for less important stuff that will take time.
  );

  timer = timerBegin(0, 80,true); // 1 tick = 1 microsedcond if clock standard is 80 MHZ: 80MHZ/80 = 1MHZ: run at 1 MHZ for each tick, 10^-6 seconds: for what 500Hz sampling: 0.002 seconds (2 milliseconds) 2000 microseconds to 2 milliseconds

  timerAttachInterrupt(timer, &onTimer, true); //attach ISR task 

  timerAlarmWrite(timer, 2000, true); //2000 ticks, true for count up 

  timerAlarmEnable(timer);



  vTaskDelete(NULL); //cancel loop, and setup() has already run.

}

void loop() {
  
  //loop will not run because of line 354

}
