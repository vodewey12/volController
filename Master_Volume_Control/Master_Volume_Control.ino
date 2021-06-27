int serialValues[2];

void setup()
{
  Serial.begin(9600);
  pinMode(2, INPUT);
}

void loop()
{

  updateValues();
  parseValues();
}

void updateValues()
{
  serialValues[0] = digitalRead(2);

  serialValues[1] = analogRead(A0);
}

void parseValues()
{
  String builtString = String("");

  for (int i = 0; i < 2; i++)
  {
    builtString += String((int)serialValues[i]);

    if (i < 1)
    {
      builtString += String("|");
    }
  }

  Serial.println(builtString);
}