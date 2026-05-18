##  Math (Int) (Text-Driven)

An advanced integer arithmetic core designed to calculate loops, steps, dimensions, and indexing logic safely.

* **Inputs:**
* `a` / `b` (Int, Range: `-999,999,999` to `999,999,999`): Supports massive negative and positive integer ranges.
* `operation` (Combo Select): `add`, `subtract`, `multiply`, `divide`, `modulo`, `power`, `shift`.


* **Advanced Logic:**
* `divide` / `modulo`: Allows natural zero-division runtime exceptions to propagate upstream safely.
* `power`: Implements safety range-guards to prevent system-freezing overflow.
* `shift` (Smart Bit-Shift): Intelligently reads the sign of `b`. Performs a standard Left Shift (`a << b`) if `b >= 0`, and automatically switches to a Right Shift (`a >> abs(b)`) if `b < 0` (capped safely at 31 bits).
