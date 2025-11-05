int LED_verde = 9;
int LED_amarelo = 10;
int LED_vermelho = 11;
int botao = 3;
int campainha = 4;
int tempo_delay = 50;
int sensor = A5;

int PORTA_A = 13;
int PORTA_B = 7;
int PORTA_C = 12;
int PORTA_D = 5;
int PORTA_E = 4;
int PORTA_F = 8;
int PORTA_G = 6;
int PORTA_DP1 = 2;
int PORTA_DP2 = 3;

int contador = 0;

void displayDigit(int digit, int pos) {
  // Matriz de segmentos para cada dígito (0-9)
  const int digits[10][7] = {
    {1, 1, 1, 1, 1, 1, 0},  // 0
    {0, 1, 1, 0, 0, 0, 0},  // 1
    {1, 1, 0, 1, 1, 0, 1},  // 2
    {1, 1, 1, 1, 0, 0, 1},  // 3
    {0, 1, 1, 1, 0, 1, 1},  // 4
    {1, 0, 1, 1, 0, 1, 1},  // 5
    {1, 0, 1, 1, 1, 1, 1},  // 6
    {1, 1, 1, 0, 0, 0, 0},  // 7
    {1, 1, 1, 1, 1, 1, 1},  // 8
    {1, 1, 1, 1, 0, 1, 1}   // 9
  };

  // Escolher qual dígito (dezena ou unidade) controlar
  if (pos == 1) {  // Primeiro dígito (dezena)
    digitalWrite(PORTA_DP1, LOW);  // Desligar o ponto decimal no primeiro dígito
    digitalWrite(PORTA_DP2, HIGH); // Manter o ponto decimal no segundo dígito
  } else {  // Segundo dígito (unidade)
    digitalWrite(PORTA_DP1, HIGH);  // Manter o ponto decimal no primeiro dígito
    digitalWrite(PORTA_DP2, LOW);   // Desligar o ponto decimal no segundo dígito
  }

  // Controlar os segmentos para exibir o número
  digitalWrite(PORTA_A, digits[digit][0]);
  digitalWrite(PORTA_B, digits[digit][1]);
  digitalWrite(PORTA_C, digits[digit][2]);
  digitalWrite(PORTA_D, digits[digit][3]);
  digitalWrite(PORTA_E, digits[digit][4]);
  digitalWrite(PORTA_F, digits[digit][5]);
  digitalWrite(PORTA_G, digits[digit][6]);
}





void setup() {
  // put your setup code here, to run once:
  pinMode(LED_verde, OUTPUT);
  pinMode(LED_amarelo, OUTPUT);
  pinMode(LED_vermelho, OUTPUT);
  pinMode(botao, INPUT);
  pinMode(campainha, OUTPUT);

  pinMode(PORTA_A, OUTPUT);
  pinMode(PORTA_B, OUTPUT);
  pinMode(PORTA_C, OUTPUT);
  pinMode(PORTA_D, OUTPUT);
  pinMode(PORTA_E, OUTPUT);
  pinMode(PORTA_F, OUTPUT);
  pinMode(PORTA_G, OUTPUT);
  pinMode(PORTA_DP1, OUTPUT);
  pinMode(PORTA_DP2, OUTPUT);



  pinMode(sensor, INPUT);
  Serial.begin(115200);
}
/*
void loop() {
  int sensorValue = analogRead(sensor); // Lê o valor do sensor
  int number = map(sensorValue, 0, 1023, 0, 99); // Mapeia o valor do sensor para um número entre 0 e 99
  
  // Declarar as variáveis tens e ones (dezena e unidade)
  int tens = number / 10;  // Dezena
  int ones = number % 10;  // Unidade





  Serial.println(analogRead(sensor));
  delay(1);
  if (analogRead(sensor) >1024){
    digitalWrite(LED_vermelho, HIGH);
    //digitalWrite(LED_amarelo, HIGH);
    digitalWrite(LED_verde, LOW);
    Serial.println("HIGH");
    Serial.println(analogRead(sensor));


    displayDigit(tens, 2);  // Exibe a dezena no primeiro dígito
    //displayDigit(ones, 2);

  }else{
    digitalWrite(LED_vermelho, LOW);
    //digitalWrite(LED_amarelo, LOW);
    digitalWrite(LED_verde, HIGH);
    Serial.println("LOW");
    displayDigit(tens, 2);
    //displayDigit(3);
  }
}

*/
void loop() {
  digitalWrite(8, HIGH);
  


  Serial.println(analogRead(sensor));
  delay(1);
  if (analogRead(sensor) >900){
    Serial.println("SENSOR_ATIVADO");
    digitalWrite(PORTA_A, HIGH);

    digitalWrite(LED_amarelo, LOW);
    digitalWrite(LED_vermelho, HIGH);
    digitalWrite(LED_verde, LOW);

    contador++;
    if (contador > 99) contador = 99;
    
    delay(1000);
    //digitalWrite(LED_amarelo, HIGH);
    //digitalWrite(LED_verde, LOW);
    Serial.println("HIGH");
    Serial.println(analogRead(sensor));


    //displayDigit(tens, 2);  // Exibe a dezena no primeiro dígito
    //displayDigit(ones, 2);

  }else if (analogRead(sensor) > 100){
    digitalWrite(LED_vermelho, LOW);
    digitalWrite(LED_verde, LOW);
    digitalWrite(LED_amarelo, HIGH);
    delay(2000);
  }else{
    digitalWrite(LED_amarelo, LOW);
    digitalWrite(LED_vermelho, LOW);
    digitalWrite(LED_verde, HIGH);

    digitalWrite(PORTA_A, LOW);
    //digitalWrite(LED_vermelho, LOW);
    //digitalWrite(LED_amarelo, LOW);
    //digitalWrite(LED_verde, HIGH);
    Serial.println("LOW");
    //displayDigit(tens, 2);
    //displayDigit(3);
  }

  int dezena = contador / 10;
  int unidade = contador % 10;

  // Multiplexar os dois dígitos rapidamente (ex: 10 vezes para persistência visual)
  for (int i = 0; i < 10; i++) {
    displayDigit(unidade, 1);  // Mostra dezena no primeiro dígito
    delay(5);  // Pequeno delay para persistência visual

    displayDigit(dezena, 2);  // Mostra unidade no segundo dígito
    delay(5);
  }
}