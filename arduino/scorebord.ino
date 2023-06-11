#include <DMD.h>
#include <Arial_black_16.h>

DMD display(7,4);
boolean piConnected = false;

ISR(TIMER1_OVF_vect)
{
    display.refresh();
}

void initScreen() {
    display.setFont(Arial_Black_16);
    display.drawText(48, 38, "WSB Apeldoorn");
}


void setup() {
  initScreen();
  Serial.begin(9600, SERIAL_8N1);
  display.setDoubleBuffer(true);
  display.enableTimer1();    
}

void loop() {
  if(Serial.available() > 0) {

    if(!piConnected) {
      char startChar = Serial.read();
      if(startChar = '<') {
        String ip = Serial.readStringUntil('>');
        display.clear();
        display.setFont(Arial_Black_16);
        display.drawText(60, 18, ip);
        display.drawText(48, 38, "WSB Apeldoorn");
        display.swapBuffers();
        piConnected = true;
      }
    }else{   
      byte buf[display.screenSizeInBytes()];
      Serial.readBytes(buf,sizeof(buf));
  
      /*for(int i = 0; i < sizeof(buf); i++) {
        Serial.print(buf[i],HEX);
        Serial.print(",");
      }
      Serial.println();*/
      
          
      display.clear(); //clear het oude frame eerst
      //for(int i = 0; i < sizeof(buf); i++) {
        //display.writeByteAtIndex((int)buf[i],i);
      //}
      memcpy(display.getDrawingPointer(),&buf, sizeof(buf));
      display.swapBuffers();
      Serial.println("Displaying new content");
    }
  }
}
