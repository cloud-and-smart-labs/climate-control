
#include <Arduino_HTS221.h>
#include <Arduino_LPS22HB.h>
#include <Arduino_APDS9960.h>

void setup()
{
  Serial.begin(9600);
  while (!Serial)
    ;

  if (!HTS.begin())
  {
    Serial.println("Failed to initialize humidity temperature sensor!");
    while (1)
      ;
  }

  if (!BARO.begin())
  {
    Serial.println("Failed to initialize pressure sensor!");
    while (1)
      ;
  }

  if (!APDS.begin())
  {
    Serial.println("Error initializing APDS9960 sensor.");
  }
}

void loop()
{
  float temperature = HTS.readTemperature();
  float humidity = HTS.readHumidity();

  float pressure = BARO.readPressure();
  float altitude = 44330 * (1 - pow(pressure / 101.325, 1 / 5.255));

  int r, g, b;
  while (!APDS.colorAvailable())
  {
    delay(5);
  }
  APDS.readColor(r, g, b);

  Serial.print("Temperature:");
  Serial.println(temperature);
  Serial.print("Humidity:");
  Serial.println(humidity);

  Serial.print("pressure:");
  Serial.println(pressure);
  Serial.print("altitude:");
  Serial.println(altitude);

  Serial.print("light_red:");
  Serial.println(r);
  Serial.print("light_green:");
  Serial.println(g);
  Serial.print("light_blue:");
  Serial.println(b);

  Serial.println();
  delay(1000);
}
