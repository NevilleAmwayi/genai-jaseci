import from byllm.llm {Model}

#Initialize the LLM
glob llm = Model(model_name="gemini/gemini-2.0-flash", verbose=False);

#Function to handle the math logic
def calculate(num1: float, num2: float, operator: str) -> str by llm();

walker Calculator {
    has num1: float;
    has num2: float;
    has operator: str;

    can start with `root entry;
    can perform_calculation with turn entry;
}

node turn {}

with entry:__main__ {
    # Ask the user for input
    n1 = float(input("Enter first number: "));
    n2 = float(input("Enter second number: "));
    op = input("Enter operator (+, -, *, /): ");

    # Spawn calculator with user inputs
    root spawn Calculator(n1, n2, op);
}