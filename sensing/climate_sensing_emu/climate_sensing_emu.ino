
void setup()
{
  Serial.begin(9600);
  while (!Serial)
    ;
}

void loop()
{
  float temperature = random(15, 50);
  float humidity = random(10, 100);

  float pressure = random(80, 90);
  float altitude = 44330 * (1 - pow(pressure / 101.325, 1 / 5.255));

  int r, g, b;
  r = random(0, 255);
  g = random(0, 255);
  b = random(0, 255);
  
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
