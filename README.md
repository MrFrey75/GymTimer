# GymTimer 💪⏱️

Dead‑simple Arduino‑based gym timer built for StrongLifts 5×5 (or any set‑focused routine). Perfect for tracking rest between sets with LEDs and buzzer—no fuss, no fluff.

---

## 🚀 Features

- **Set counter** LEDs: Visualize how many sets remain (up to 10).
- **Rest timer**: Audible buzzer signals the end of rest.
- **Handy cancel**: Press the button during rest to skip remaining time.
- **Loop friendly**: Automatically restarts for another round of sets.
- **Fully customizable**: Adjust rest duration and number of sets directly in the `.ino`.

---

## 🔧 Hardware Requirements

- Arduino Uno (or similar)
- 5–10 LEDs + ~220 Ω resistors
- Piezo buzzer
- Push-button switch (momentary)
- Hookup wires & breadboard

---

## 🧩 Wiring Guide

| Component     | Arduino Pin       | Details                            |
|---------------|-------------------|------------------------------------|
| LEDs #1–#5    | Pins 3 → 7         | 220 Ω resistor to ground each      |
| Extra LEDs (optional) | Pins 9 → 13   | Another bank (max 10 LEDs total)  |
| Buzzer        | Pin 8 → GND       | Piezo buzzer                       |
| Push-button   | Pin 2 → GND       | Use internal pull-up resistor      |

---

## 💾 Code & Configuration

In `gym_timer.ino`, tune:

```cpp
const uint32_t REST_PERIOD_MS = 90 * 1000;   // ~90-second rest
const uint8_t  MAX_SETS        = 5;          // number of sets
