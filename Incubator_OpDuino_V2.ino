int PA = 12; // Peltier A
int PB = 13; // Peltier B
int temp1 = A0; // Peltier Temp A
int temp2 = A1; // Chamber Temp A
int temp3 = A2; // Culture Temp A
int temp4 = A3; // Peltier Temp B
int temp5 = A4; // Chamber Temp B
int temp6 = A5; // Culture Temp B

String p1="\t";
int T1;
int T2;
int T3;
int T4;
int T5;
int T6;
void setup () {
   pinMode(PA, INPUT); 
   pinMode(PB, INPUT); 
   pinMode(temp1, INPUT);
   pinMode(temp2,INPUT); 
   pinMode(temp3, INPUT);
   pinMode(temp4, INPUT);
   pinMode(temp5, INPUT);
   pinMode(temp6, INPUT);
   Serial.begin(9600); //
}

void loop () {
   T1 = analogRead(0);
   T2 = analogRead(1);
   T3 = analogRead(2);
   T4 = analogRead(3);
   T5 = analogRead(4);
   T6 = analogRead(5);
   Serial.println(T1 + p1 + T2 + p1 + T3 + p1 + T4 + p1 + T5 + p1 + T6);
   if (Serial.available()) { //   # Read serial Input for Command
      char c = Serial.read(); //
      pinMode(PA, OUTPUT); 
      pinMode(PB, OUTPUT);
      if (c == 'A') { //
         digitalWrite(PA, LOW);
      } else if (c == 'a') { 
         digitalWrite(PA, HIGH);
      }else if (c == 'B') { //
         digitalWrite(PB, LOW);
      }else if (c == 'b') { //
         digitalWrite(PB, HIGH);
      }
   }
   
}
