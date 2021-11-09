int serialValues[4];

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
  serialValues[2] = analogRead(A1);
  serialValues[3] = analogRead(A2);
}

void parseValues()
{
  String builtString = String("");

  for (int i = 0; i < 4; i++)
  {
    builtString += String((int)serialValues[i]);

    if (i < 3)
    {
      builtString += String("|");
    }
  }

  Serial.println(builtString);
}
