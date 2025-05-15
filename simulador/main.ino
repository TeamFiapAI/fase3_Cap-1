#include <DHT.h>

#define DHTPIN 23
#define DHTTYPE DHT22

const int pinFosforo = 22;
const int pinPotassio = 17;
const int pinPH = 32;       // LDR
const int pinRele = 25;     // Relé

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);

  //Botoes
  pinMode(pinFosforo, INPUT_PULLUP);
  pinMode(pinPotassio, INPUT_PULLUP);
  
  
  pinMode(pinPH, INPUT);
  pinMode(pinRele, OUTPUT);
  dht.begin();

  Serial.println("Sistema de Monitoramento Agrícola Iniciado");
}

void loop() {
  // Simuladores de Fosforo e Potassio
  bool fosforoPresente = digitalRead(pinFosforo) == LOW;
  bool potassioPresente = digitalRead(pinPotassio) == LOW;
  
  // valor entre 0 e 4095
  int valorLDR = analogRead(pinPH);
  // Mapeia para escala de pH entre 0 e 14
  float valorPH = map(valorLDR, 0, 4095, 0, 1400) / 100.0;
  
  float umidade = dht.readHumidity();
  float temperatura = dht.readTemperature();

  // Possivel Erro de Leitura
  if (isnan(umidade) || isnan(temperatura)) {
      Serial.println("Falha ao ler do sensor DHT!");
      return;
  }

  Serial.print("Fósforo: ");
  Serial.println(fosforoPresente ? "Sim" : "Não");

  Serial.print("Potássio: ");
  Serial.println(potassioPresente ? "Sim" : "Não");

  Serial.print("pH: ");
  Serial.println(valorPH);

  Serial.print("Umidade: ");
  Serial.print(umidade);
  Serial.println(" %");

  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println(" *C");

  // LOGICA PARA LIGAR IRRIGACAO
  if (umidade < 40) {
    digitalWrite(pinRele, HIGH);
    Serial.println("🚿 Irrigação ATIVADA");
  } else {
    digitalWrite(pinRele, LOW);
    Serial.println("❌ Irrigação DESATIVADA");
  }

  Serial.println("-------------------------------");
  delay(5000);
}