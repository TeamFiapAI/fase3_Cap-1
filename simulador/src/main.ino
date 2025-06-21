#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <HTTPClient.h>

#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASSWORD ""
#define SERVER_URL "http://192.168.68.61:8000/dados/"

#define DHTPIN 23
#define DHTTYPE DHT22
#define PIN_PH 32
#define PIN_RELE 25
#define PIN_FOSFORO 18
#define PIN_POTASSIO 16


DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

String getIdentificador() {
  return "HUM-S123";
}

void conectarWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Conectando ao WiFi");

  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 20) {
    delay(500);
    Serial.print(".");
    tentativas++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi conectado: " + WiFi.localIP().toString());
  } else {
    Serial.println("Falha ao conectar ao WiFi.");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Falha WiFi");
    delay(2000);
    lcd.clear();
  }
}

void setup() {
  Serial.begin(115200);
  
  dht.begin();

  Wire.begin(21, 22);
  lcd.init();
  lcd.backlight();

  pinMode(PIN_FOSFORO, INPUT_PULLUP);
  pinMode(PIN_POTASSIO, INPUT_PULLUP);
  pinMode(PIN_PH, INPUT);
  pinMode(PIN_RELE, OUTPUT);

  conectarWiFi();

  lcd.setCursor(0, 0);
  lcd.print("Monitor Iniciado");
  delay(2000);
  lcd.clear();
}

void loop() {
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

  bool irrigacao = false;
  if (umidade < 40.0) {
    digitalWrite(PIN_RELE, HIGH);
    irrigacao = true;
  } else {
    digitalWrite(PIN_RELE, LOW);
  }

  lcd.setCursor(0, 0);
  lcd.print("U:");
  lcd.print((uint8_t)umidade);
  lcd.print("% pH:");
  lcd.print(valorPH, 1);

  lcd.setCursor(0, 1);
  lcd.print("PK:");
  lcd.print(fosforo ? "P" : "-");
  lcd.print(potassio ? "K" : "-");
  lcd.print(" ");
  lcd.print(irrigacao ? "ON " : "OFF");

  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.print("°C  |  Umidade: ");
  Serial.print(umidade);
  Serial.println("%");

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");

    String payload = "{";
    payload += "\"temperatura\":" + String(temperatura, 1) + ",";
    payload += "\"umidade\":" + String(umidade, 1) + ",";
    payload += "\"ph\":" + String(valorPH, 1) + ",";
    payload += "\"fosforo\":" + String(fosforo ? "true" : "false") + ",";
    payload += "\"potassio\":" + String(potassio ? "true" : "false") + ",";
    payload += "\"modelo\":\"" + getIdentificador() + "\"";
    payload += "}";

    int httpResponseCode = http.POST(payload);
    Serial.println("POST enviado | Código HTTP: " + String(httpResponseCode));
    Serial.println("Payload: " + payload);

    http.end();
  }

  delay(200);
}
