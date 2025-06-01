import re
import sys
import pascal_lex
import pascal_sin
from pascal_lex import lexer
from pascal_sin import parser, syntax_errors
from translator import Translator


def main():
    files = [
        "Fatorial.pas",
        "Mundo_talk.pas",
        "NestedIf.pas",
        "readln.pas",
        "SomaArray.pas",
        "String.pas",
        "Varios_prints.pas",
        "while.pas",
        "BooleanTest.pas"
    ]
    print("This CLI was brought to you by Group 53 for demonstration purposes only!\n")
    while True:
        print("Please Select your Pascal Code:")
        for idx, fname in enumerate(files, start=1):
            print(f"{idx}. {fname}")
        print("0. Quit\n")
        choice = input("Choose wisely: ").strip()
        if not re.match(r'^[0-9]+$', choice):
            print("Invalid input. Please enter an integer.\n")
            continue
        choice_int = int(choice)
        if choice_int == 0:
            print("Bye! Have a Beautiful Time!")
            sys.exit(0)
        if 1 <= choice_int <= len(files):
            filename = files[choice_int - 1]
            break
        else:
            print(f"Invalid choice. Please enter a number between 0 and {len(files)}.\n")

    # Read input file
    try:
        with open("../tests/" + filename, "r") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"File '../tests/{filename}' not found.")
        sys.exit(1)

   # Parse input
    parser = pascal_sin.parser
    parser.success = True
    ast = parser.parse(code, lexer=pascal_sin.lexer)
    if syntax_errors:
        parser.success = False
        for e in syntax_errors:
            print(e)

    if parser.success:
        # Translate AST to VM code
        print("AST:", ast)
        translator = Translator()
        vm_code = translator.translate_program(ast)
        # print(translator.symbol_table.variables)

        print("Generated VM Code:")
        for line in vm_code:
            print(line)

        with open("../results/Output.txt", "w") as f:
            f.write("\n".join(vm_code))
    else:
        print("Translation failed due to parsing errors.")


if __name__ == "__main__":
    main()