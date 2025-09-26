impl calculate {
    if operator == "+" {
        return f"The result is {num1 + num2}";
    } elif operator == "-" {
        return f"The result is {num1 - num2}";
    } elif operator == "*" {
        return f"The result is {num1 * num2}";
    } elif operator == "/" {
        if num2 == 0 {
            return "Error: Division by zero is not allowed.";
        }
        return f"The result is {num1 / num2}";
    } else {
        return "Invalid operator. Please use +, -, * or /.";
    }
}

impl Calculator.start {
    if not [root --> (`?turn)] {
        next = root ++> turn();
    } else {
        next = [root --> (`?turn)];
    }
    visit next;
}

impl Calculator.perform_calculation{
    if [-->] {
        visit [-->];
    } else {
        print(calculate(self.num1, self.num2, self.operator));
        disengage;
    }
}