#include <DHT.h>
#include <WiFi.h>


#define DHTPIN 23
#define DHTTYPE DHT22

const int pinFosforo = 22;
const int pinPotassio = 17;
const int pinPH = 32;       // LDR
const int pinRele = 25;     // Relé

DHT dht(DHTPIN, DHTTYPE);

String getIdentificador() {
  uint64_t chipid = ESP.getEfuseMac(); // Pega o MAC (64 bits)
  char id[20];
  snprintf(id, sizeof(id), "%04X%08X", (uint16_t)(chipid >> 32), (uint32_t)chipid);
  return String(id);
}

String identificador;

void setup() {
  Serial.begin(9600);
  identificador = getIdentificador();
  
  //Botoes
  pinMode(pinFosforo, INPUT_PULLUP);
  pinMode(pinPotassio, INPUT_PULLUP);
  pinMode(pinPH, INPUT);
  pinMode(pinRele, OUTPUT);
  dht.begin();

  Serial.println("Sistema de Monitoramento Agricola Iniciado");
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

  Serial.print("Fosforo: ");
  Serial.println(fosforoPresente ? "Sim" : "Nao");

  Serial.print("Potassio: ");
  Serial.println(potassioPresente ? "Sim" : "Nao");

  Serial.print("pH: ");
  Serial.println(valorPH);

  Serial.print("Umidade: ");
  Serial.print(umidade);
  Serial.println(" %");

  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println(" *C");

  // LOGICA PARA LIGAR IRRIGACAO
  bool irrigacao = false;
  if (umidade < 40) {
    digitalWrite(pinRele, HIGH);
    Serial.println("[ON] Irrigacao ATIVADA");
    irrigacao = true;
  } else {
    digitalWrite(pinRele, LOW);
    Serial.println("[OFF] Irrigacao DESATIVADA");
  }

  Serial.println("---------------------------------------");

  Serial.print(identificador);
  Serial.print(";");
  Serial.print(fosforoPresente ? 't' : 'f');
  Serial.print(";");
  Serial.print(potassioPresente ? 't' : 'f');
  Serial.print(";");
  Serial.print(valorPH, 2);
  Serial.print(";");
  Serial.print(umidade, 2);
  Serial.print(";");
  Serial.print(temperatura, 2);
  Serial.print(";");
  Serial.println(irrigacao ? 't' : 'f');
  Serial.println("---------------------------------------");
  Serial.println("");
  delay(5000);
}