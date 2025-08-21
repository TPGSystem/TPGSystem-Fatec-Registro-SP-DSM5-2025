const int pinX = A0;
const int pinY = A1;
const int pinButton = 2;

const char* xtexto;
const char* ytexto;

void setup() {
  Serial.begin(9600);         
  pinMode(pinButton, INPUT_PULLUP);  
}

void loop() {
  int xValue = analogRead(pinX);     // Lê o valor do eixo X
  int yValue = analogRead(pinY);     // Lê o valor do eixo Y
  int buttonState = digitalRead(pinButton); // Lê o estado do botão

  xtexto = buttonState == LOW ? "ACTION" : "STOP";

  if (xValue >= 520) {
    xtexto = "LEFT";
  } else {
    if (xValue <= 450) {
      xtexto = "RIGHT";
    } else {
      if (yValue >= 520) {
        xtexto = "DOWN";
      } else {
        if (yValue <= 450) {
          xtexto = "UP";
        }
      }
    }
  }

  Serial.println(xtexto);

  delay(400);
}