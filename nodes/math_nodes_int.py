from comfy_api.latest import io

class MathInt(io.ComfyNode):
    """
    Part of 'ComfyUI Text-Driven Workflows'.
    Integer arithmetic node.
    - Supports negative inputs.
    - Smart shift: Left shift if B > 0, Right shift if B < 0.
    - Direct error raising for zero division.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TextDrivenMathInt",
            display_name="Math (Int) (Text-Driven)",
            category="Text-Driven Workflows",
            inputs=[
                # Support large negative and positive integers
                io.Int.Input("a", default=0, min=-999999999, max=999999999),
                io.Int.Input("b", default=0, min=-999999999, max=999999999),
                io.Combo.Input(
                    "operation",
                    options=["add", "subtract", "multiply", "divide", "modulo", "power", "shift"],
                    default="add"
                ),
            ],
            outputs=[
                io.Int.Output("int_out")
            ],
        )

    @classmethod
    def execute(cls, a: int, b: int, operation: str) -> io.NodeOutput:
        """
        Calculates the result.
        Now allows runtime errors to propagate for division/modulo by zero.
        """
        a_val = int(a)
        b_val = int(b)
        result = 0

        if operation == "add":
            result = a_val + b_val
        elif operation == "subtract":
            result = a_val - b_val
        elif operation == "multiply":
            result = a_val * b_val
        elif operation == "divide":
            # Raises ZeroDivisionError naturally if b_val is 0
            result = a_val // b_val
        elif operation == "modulo":
            # Raises ZeroDivisionError naturally if b_val is 0
            result = a_val % b_val
        elif operation == "power":
            # Negative exponents would result in floats, so we keep them as 0 or error
            # but standardizing for Int utility:
            safe_b = min(max(b_val, 0), 32)
            result = a_val ** safe_b
        elif operation == "shift":
            if b_val >= 0:
                # Standard Left Shift (up to 31 bits for safety)
                safe_b = min(b_val, 31)
                result = a_val << safe_b
            else:
                # Right Shift using absolute value of B (up to 31 bits)
                safe_b = min(abs(b_val), 31)
                result = a_val >> safe_b

        return io.NodeOutput(int(result))