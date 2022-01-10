/* Button/LED Matrix Scanning Example - 3x3 Keypad
   Code derived from Button Pad Hookup Guide Example 2
   by Byron Jacquot @ SparkFun Electronics
     https://learn.sparkfun.com/tutorials/button-pad-hookup-guide#exercise-2-monochrome-plus-buttons
*/
//////////////////////
// Config Variables //
//////////////////////
#define NUM_BTN_COLS (7) // Number of switch columns (isolating diode anode)
#define NUM_BTN_ROWS (1) // Number of switch rows (isolating diode cathode)

// Debounce built-in to the code. This sets the number of button
// high or low senses that trigger a press or release
#define MAX_DEBOUNCE (1)

////////////////////
// Hardware Setup //
////////////////////
static const uint8_t btnRowPins[NUM_BTN_ROWS] = {2}; // Pins connected to switch rows (2)
static const uint8_t btnColPins[NUM_BTN_COLS] = {3, 4, 5, 6, 7, 8, 9}; // Pins connected to switch columns (1)

//////////////////////
// Global Variables //
//////////////////////
static int8_t debounce_count[NUM_BTN_COLS][NUM_BTN_ROWS]; // One debounce counter per switch

int serialValues[4];

void setup()
{
  Serial.begin(9600);
  //pinMode(2, INPUT);

  setupSwitchPins();

  // Initialize the debounce counter array
  for (uint8_t i = 0; i < NUM_BTN_COLS; i++)
  {
    for (uint8_t j = 0; j < NUM_BTN_ROWS; j++)
    {
      debounce_count[i][j] = 0;
    }
  }
}

void loop()
{

  updateValues();
  parseValues();
}

void updateValues()
{
  //serialValues[0] = digitalRead(2);
  serialValues[0] = analogRead(A0);
  serialValues[1] = analogRead(A1);
  serialValues[2] = analogRead(A2);
  serialValues[3] = analogRead(A3);

}

void parseValues()
{
  String builtString = String("");
  static uint8_t currentRow = 0;
  uint8_t i, j; // for loop counters
  digitalWrite(btnRowPins[currentRow], LOW);
  for (int i = 0; i < 4; i++)
  {
    builtString += String((int)serialValues[i]);

    if (i < 4)
    {
      builtString += String("|");
    }
  }

  for ( j = 0; j < NUM_BTN_COLS; j++)
  {
    // Read the button. If it's pressed, it should be LOW.
    if (digitalRead(btnColPins[j]) == LOW)
    {
      if ( debounce_count[currentRow][j] < MAX_DEBOUNCE)
      { // Increment a debounce counter
        debounce_count[currentRow][j]++;
        if ( debounce_count[currentRow][j] == MAX_DEBOUNCE )
        { // If debounce counter hits MAX_DEBOUNCE (default: 3)
          // Trigger key press -- Do anything here...
          builtString += "Key pressed " + String((currentRow * NUM_BTN_COLS) + j);

        }
      }
    }
    else // Otherwise, button is released
    {
      if ( debounce_count[currentRow][j] > 0)
      {
        debounce_count[currentRow][j]--; // Decrement debounce counter
        if ( debounce_count[currentRow][j] == 0 )
        { // If debounce counter hits 0
          // Trigger key release -- Do anything here...
          builtString += "Key released " + String((currentRow * NUM_BTN_COLS) + j);
        }
      }
    }
  }

  // Once done scanning, de-select the switch and LED rows
  // by writing them HIGH.
  digitalWrite(btnRowPins[currentRow], HIGH);
  Serial.println(builtString);
  delay(100);
}

static void scan()
{
  // Each run through the scan function operates on a single row
  // of the matrix, kept track of using the currentRow variable.


  // Select current row, and write all components on that row LOW.
  // That'll set the LED anode's LOW, and write the switch "2" pins LOW.
  // If diodes were added, "2' should be connected to the diode cathode



  // Scan through switches on this row:

  // Increment currentRow, so next time we scan the next row
}

static void setupSwitchPins()
{
  uint8_t i;

  // Button drive rows - written LOW when active, HIGH otherwise
  for (i = 0; i < NUM_BTN_ROWS; i++)
  {
    pinMode(btnRowPins[i], OUTPUT);

    // with nothing selected by default
    digitalWrite(btnRowPins[i], HIGH);
  }

  // Buttn select columns. Pulled high through resistor. Will be LOW when active
  for (i = 0; i < NUM_BTN_COLS; i++)
  {
    pinMode(btnColPins[i], INPUT_PULLUP);
  }
}
