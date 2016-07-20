// ################################################################
// ####################  LCD DRIVER  ##############################
// ################################################################


// THESE PINS ARE SET UP FOR THE MAPLE MINI STM32DUINO
// They probably work for other arduinos (avr),
// but are untested and may overlap important pins.

#define PIN_SCE   PB7
#define PIN_RESET PB6
#define PIN_DC    PB5
#define PIN_SDIN  PB4
#define PIN_SCLK  PB3

#define LCD_C     LOW
#define LCD_D     HIGH

#define LCD_X     84
#define LCD_Y     48


void LcdClear(void)
{
  #define lcd_com_xaddr 1 << 7
  #define lcd_com_yaddr 1 << 6

  LcdWrite(LCD_C, lcd_com_xaddr );//& 0 )
  LcdWrite(LCD_C, lcd_com_yaddr );//& 0 )
  for (int index = 0; index < LCD_X * LCD_Y / 8; index++)
  {
    LcdWrite(LCD_D, 0x00);
  }
}

void LcdWrite(byte dc, byte data)
{
  digitalWrite(PIN_DC, dc);
  digitalWrite(PIN_SCE, LOW);
  shiftOut(PIN_SDIN, PIN_SCLK, MSBFIRST, data);
  digitalWrite(PIN_SCE, HIGH);
}

void LcdInitialise(void)
{
  pinMode(PIN_SCE, OUTPUT);
  pinMode(PIN_RESET, OUTPUT);
  pinMode(PIN_DC, OUTPUT);
  pinMode(PIN_SDIN, OUTPUT);
  pinMode(PIN_SCLK, OUTPUT);
  digitalWrite(PIN_RESET, LOW);
  digitalWrite(PIN_RESET, HIGH);
  LcdWrite(LCD_C, 0x21 );  // LCD Extended Commands.
  LcdWrite(LCD_C, 0xB1 );  // Set LCD Vop (Contrast). 
  LcdWrite(LCD_C, 0x04 );  // Set Temp coefficent. //0x04
  LcdWrite(LCD_C, 0x14 );  // LCD bias mode 1:48. //0x13
  LcdWrite(LCD_C, 0x20 );  // LCD Basic Commands
  LcdWrite(LCD_C, 0x0C );  // LCD in normal mode.
}

// ################################################################
// ###################### LCD DRIVER END ##########################
// ################################################################


#define LED_1 PB1
#define MY_BAUD_RATE 115200


int serial_mode = false;
int serial_init = true;
volatile int recv_count = 0;


void setup(void)
{
  LcdInitialise();
  LcdClear();

  pinMode(LED_1, OUTPUT);
  digitalWrite(LED_1, HIGH);

  Serial.begin(MY_BAUD_RATE);
}


int scount = 0;

void loop(void)
{

  scount = Serial.available();
  if (serial_init){
    
    Serial.println("Ready");
    
    if (Serial.available() > 0){
      serial_init = false;
      LcdClear();
    }

  }else{

    if (recv_count < 504){
      if (scount > 0){
        byte inByte = Serial.read();
        LcdWrite(LCD_D, inByte);
        recv_count++; 
        if (recv_count % 126 == 0){
          delay(2);
        }
      }
    }else{
      delay(1000);
      serial_mode = false;
      serial_init = true;
      recv_count = 0;
    }

  }

}


