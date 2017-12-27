//////
// speed up sampling rate -- by [url=mailto:tsaiwn@cs.nctu.edu.tw]tsaiwn@cs.nctu.edu.tw[/url]
const int pin = A0;
int data;
void setup() {
  Serial.begin(115200);
  
}
void loop( ) { 
     data=analogRead(pin);
     Serial.println(data);
     delayMicroseconds(150);
  
}
