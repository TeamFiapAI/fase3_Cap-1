#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>

// Umidade
#define DHTPIN 23
#define DHTTYPE DHT22
// Rele
#define PIN_PH 32
#define PIN_RELE 25

// Potassio e Fosforo
#define PIN_FOSFORO 18
#define PIN_POTASSIO 16

// Inicialização de componentes
DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2); // Endereço padrão 0x27

void setup() {
  Serial.begin(115200);
  
  dht.begin();

  // Configuração do LCD
  Wire.begin(21, 22);
  lcd.init();
  lcd.backlight();

  // GPIO de entrada com pull-up para botões
  pinMode(PIN_FOSFORO, INPUT_PULLUP);
  pinMode(PIN_POTASSIO, INPUT_PULLUP);

  // LDR e relé
  pinMode(PIN_PH, INPUT);
  pinMode(PIN_RELE, OUTPUT);

  lcd.setCursor(0, 0);
  lcd.print("Monitor Iniciado");
  delay(2000);
  lcd.clear();
}

void loop() {
  // Entradas
  bool fosforo = digitalRead(PIN_FOSFORO) == LOW;
  bool potassio = digitalRead(PIN_POTASSIO) == LOW;

  int16_t valorLDR = analogRead(PIN_PH);
  float valorPH = map(valorLDR, 0, 4095, 0, 1400) / 100.0;

  float umidade = dht.readHumidity();
  float temperatura = dht.readTemperature();

  if (isnan(umidade) || isnan(temperatura)) {
    Serial.println("Falha ao ler o sensor DHT!");
    return;
  }

  // Lógica de irrigação
  bool irrigacao = false;
  if (umidade < 40.0) {
    digitalWrite(PIN_RELE, HIGH);
    irrigacao = true;
  } else {
    digitalWrite(PIN_RELE, LOW);
  }

  // Exibe no LCD
  lcd.setCursor(0, 0);
  lcd.print("U:");
  lcd.print((uint8_t)umidade);
  lcd.print("% pH:");
  lcd.print(valorPH, 1);

  lcd.setCursor(0, 1);
  lcd.print("NPK:");
  lcd.print(fosforo ? "F" : "-");
  lcd.print(potassio ? "K" : "-");
  lcd.print(" ");
  lcd.print(irrigacao ? "ON " : "OFF");

  // Serial Plotter
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.print("°C  |  Umidade: ");
  Serial.print(umidade);
  Serial.println("%");


  delay(5000);
}
