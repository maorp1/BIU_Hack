
#include <Servo.h>
 
Servo myservo;  // create servo object to control a servo

int angle = 10;  // analog pin used to connect the potentiometer
int val;    // variable to read the value from the analog pin
uint8_t input = 0;
int last_input = 0;
int btn_pin = 2;
int red_led = 3;
int green_led = 4;
int stat = 0;


#include <SoftwareSerial.h>  

int bluetoothTx = 9;  // TX-O pin of bluetooth mate, Arduino D2
int bluetoothRx = 10;  // RX-I pin of bluetooth mate, Arduino D3

SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);



void setup()
{


  Serial.begin(9600);  // Begin the serial monitor at 9600bps

  bluetooth.begin(115200);  // The Bluetooth Mate defaults to 115200bps
  bluetooth.print("$");  // Print three times individually
  bluetooth.print("$");
  bluetooth.print("$");  // Enter command mode
  delay(100);  // Short delay, wait for the Mate to send back CMD
  bluetooth.println("U,9600,N");  // Temporarily Change the baudrate to 9600, no parity
  // 115200 can be too fast at times for NewSoftSerial to relay the data reliably
  bluetooth.begin(9600);  // Start bluetooth serial at 9600


  
  pinMode(btn_pin, INPUT_PULLUP);
  pinMode(red_led, OUTPUT);
  pinMode(green_led, OUTPUT);
  digitalWrite(green_led, HIGH);
  digitalWrite(red_led, LOW);
  myservo.attach(9);
}
  
  void loop()
  {

    while(Serial.available()) //Check for input
    {
      bluetooth.print((char)Serial.read());
      input = 1;
    }
    
    if (input == 1) // Status change
    {
      if (stat == 1) // Red light, saved parking
      {
        angle = 10;
        digitalWrite(green_led, LOW);
        digitalWrite(red_led, HIGH);
        stat = 0;
      }
      else // Green light, open parking for saving
      {
        angle = 100;
        digitalWrite(green_led, HIGH);
        digitalWrite(red_led, LOW);
        stat = 1;
      }
      
      myservo.write(angle); // gate open/close
    last_input = input;
    }
    input = 0;
    delay(1000); // waits for the servo to get there
    
  }
