# translator.py

class SymbolTable:
    """Manages variable tracking and memory allocation."""

    def __init__(self):
        self.variables = {}
        self.global_var_counter = 0

    def allocate_var(self, var_name, var_type):
        """Allocate a new variable and return its address."""
        if var_name in self.variables:
            return self.variables[var_name]['address']

        address = self.global_var_counter

        # For arrays, allocate additional space
        if isinstance(var_type, tuple) and var_type[0] == 'array':
            self.global_var_counter += 1
        else:
            # For simple types (integer, real, string, boolean), increment by 1
            self.global_var_counter += 1

        self.variables[var_name] = {
            'address': address,
            'type': var_type
        }
        return address

    def get_var_info(self, var_name):
        """Retrieve variable information."""
        return self.variables.get(var_name)


class LabelGenerator:
    """Generates unique labels for control structures."""

    def __init__(self):
        self.counter = 0

    def generate(self, prefix='L'):
        """Generate a unique label."""
        self.counter += 1
        return f"{prefix}{self.counter}"


class ExpressionTranslator:
    """Translates expressions to VM operations."""

    def __init__(self, symbol_table, vm_code):
        self.symbol_table = symbol_table
        self.vm_code = vm_code

    def translate_numeric_constant(self, value):
        """Translate numeric constant (integer)."""
        self.vm_code.append(f"PUSHI {value}")

    def translate_string_constant(self, value):
        """Translate string constant."""
        # Uso de aspas para literal de string
        self.vm_code.append(f"PUSHS \"{value}\"")

    def translate_real_constant(self, value):
        """Translate real (float) constant."""
        self.vm_code.append(f"PUSHF {value}")

    def translate_variable_ref(self, var_name):
        """Translate variable reference."""
        var_info = self.symbol_table.get_var_info(var_name)
        if not var_info:
            raise ValueError(f"Undefined variable: {var_name}")
        self.vm_code.append(f"PUSHG {var_info['address']}")

    def translate_array_access(self, array_name, index_exp):
        """Translate array access (A[i])."""
        var_info = self.symbol_table.get_var_info(array_name)
        if not var_info:
            raise ValueError(f"Undefined array: {array_name}")

        # Empurra base address do array
        self.vm_code.append(f"PUSHG {var_info['address']}")

        # Se o índice for algo como ('var', X) ou número literal:
        if isinstance(index_exp, tuple) and index_exp[0] == 'var':
            _, var = index_exp
            var_add = self.symbol_table.variables.get(var)['address']
        else:
            var_add = index_exp

        self.vm_code.append(f"PUSHG {var_add}")
        self.vm_code.append("PUSHI 1")
        self.vm_code.append("SUB")  # corrigir índice (Pascal é 1‐based)

        # Carrega o valor em memória
        self.vm_code.append("LOADN")

    def translate_arithmetic_op(self, op, left_exp, right_exp):
        """Translate arithmetic operations (+, -, *, /, %)."""
        op_map = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIV',
            '%': 'MOD'
        }
        # Empurra operandos na pilha
        self.translate(left_exp)
        self.translate(right_exp)
        # Aplica o opcode correspondente
        self.vm_code.append(op_map[op])

    def translate_unary_op(self, op, exp):
        """Translate unary operations (uminus, not)."""
        if op == 'uminus':
            # Negativo unário: evala exp e multiplica por −1
            self.translate(exp)
            self.vm_code.append("PUSHI -1")
            self.vm_code.append("MUL")
        elif op == 'not':
            # NOT lógico: evala exp (que deve empurrar 0/1) e aplica NOT
            self.translate(exp)
            self.vm_code.append("NOT")

    def translate_relational_op(self, op, left_exp, right_exp):
        """Translate relational operations (=, <>, <, <=, >, >=)."""
        op_map = {
            '=': 'EQUAL',
            '<>': 'EQUAL NOT',
            '<': 'INF',
            '<=': 'INFEQ',
            '>': 'SUP',
            '>=': 'SUPEQ'
        }
        # Empurra operandos
        self.translate(left_exp)
        self.translate(right_exp)
        # Emite o opcode do comparador
        if op not in op_map:
            raise ValueError(f"Unsupported relational operator: {op}")
        self.vm_code.append(op_map[op])

    def translate(self, exp):
        """Main expression translation dispatch."""
        if exp is None:
            return

        # **1. Literais numéricos e reais**
        if isinstance(exp, float):
            self.translate_real_constant(exp)
            return
        if isinstance(exp, int):
            self.translate_numeric_constant(exp)
            return

        # **2. Literais booleanos** (True/False → PUSHI 1 ou PUSHI 0)
        if isinstance(exp, bool):
            val = 1 if exp else 0
            self.vm_code.append(f"PUSHI {val}")
            return

        # **3. Strings ou nomes de variáveis**
        if isinstance(exp, str):
            if exp in self.symbol_table.variables:
                self.translate_variable_ref(exp)
            else:
                # Se não for variável conhecida, assumimos que é literal de string
                self.translate_string_constant(exp)
            return

        # Se não é uma tupla neste ponto, é algo inválido
        if not isinstance(exp, tuple):
            raise ValueError(f"Unsupported expression type: {exp}")

        # **4. Se for tupla, extrai operador e argumentos**
        op = exp[0]

        if op == 'var':
            # Referência a variável
            self.translate_variable_ref(exp[1])

        elif op == 'array_access':
            # Acesso a array
            self.translate_array_access(exp[1], exp[2])

        elif op in ['+', '-', '*', '/', '%']:
            # Operador aritmético binário
            self.translate_arithmetic_op(op, exp[1], exp[2])

        elif op in ['uminus', 'not']:
            # Operador unário
            self.translate_unary_op(op, exp[1])

        elif op == 'rel':
            # Relacional: exp = ('rel', operador, esquerda, direita)
            self.translate_relational_op(exp[1], exp[2], exp[3])

        elif op == 'and':
            # AND lógico – avalia esquerda e direita, então emite AND
            self.translate(exp[1])
            self.translate(exp[2])
            self.vm_code.append("AND")
            return

        elif op == 'or':
            # OR lógico – avalia esquerda e direita, então emite OR
            self.translate(exp[1])
            self.translate(exp[2])
            self.vm_code.append("OR")
            return

        else:
            raise ValueError(f"Unsupported expression node: {exp}")


class StatementTranslator:
    """Translates statements to VM operations."""

    def __init__(self, symbol_table, vm_code, label_gen, expr_translator):
        self.symbol_table = symbol_table
        self.vm_code = vm_code
        self.label_gen = label_gen
        self.expr_translator = expr_translator

    def translate_assignment(self, stmt):
        """Translate assignment statement."""
        # stmt = ('assign', var_name, exp)
        var_name, exp = stmt[1], stmt[2]
        # Avalia o lado direito primeiro
        self.expr_translator.translate(exp)
        # Armazena no endereço da variável
        var_info = self.symbol_table.get_var_info(var_name)
        self.vm_code.append(f"STOREG {var_info['address']}")

    def translate_writeln(self, stmt):
        """Translate writeln (imprime e quebra linha)."""
        # stmt = ('writeln', lista_de_argumentos)
        if isinstance(stmt, tuple):
            self.translate_write(stmt)
        self.vm_code.append("WRITELN")

    def translate_write(self, stmt):
        """Translate write (sem quebra de linha)."""
        # stmt = ('write', [arg1, arg2, ...])
        for arg in stmt[1]:
            format_info = None
            actual_arg = arg

            # Se houver formatação (tipo: ('formatted', exp, formato)):
            if isinstance(arg, tuple) and len(arg) >= 2 and arg[0] == 'formatted':
                actual_arg = arg[1]
                if len(arg) >= 3:
                    format_info = arg[2]

            # Traduz o próprio valor
            self.expr_translator.translate(actual_arg)

            # Se tiver format_info, ainda não implementamos lógica de padding/width
            # (ignorar por enquanto)
            # ...

            # Descobre o tipo do argumento (para escolher WRITEI/WRITEF/WRITES)
            var_type = self.get_expression_type(arg)

            if var_type == 'integer':
                self.vm_code.append("WRITEI")
            elif var_type == 'real':
                self.vm_code.append("WRITEF")
            elif var_type == 'string':
                self.vm_code.append("WRITES")
            elif var_type == 'boolean':
                # Imprime booleano como inteiro (0 ou 1)
                self.vm_code.append("WRITEI")
            else:
                # Default: imprimir como inteiro
                self.vm_code.append("WRITEI")

    def get_expression_type(self, expr):
        """Determina o tipo de uma expressão AST (integer, real, string ou boolean)."""
        # 1) Se for literal booleano
        if isinstance(expr, bool):
            return 'boolean'

        # 2) Se for tupla (nodo da AST)
        if isinstance(expr, tuple):
            op = expr[0]
            # and, or, not → sempre boolean
            if op in ['and', 'or', 'not']:
                return 'boolean'
            # rela­cionais: eq/ne/lt/le/gt/ge
            if op == 'rel':
                return 'boolean'
            # aritméticos
            if op in ['+', '-', '*', '/', '%', 'uminus']:
                left_t = self.get_expression_type(expr[1])
                right_t = self.get_expression_type(expr[2]) if len(expr) > 2 else None
                if left_t == 'real' or right_t == 'real':
                    return 'real'
                return 'integer'
            # array_access
            if op == 'array_access':
                # tipo do array: var_info['type'] é algo como ('array', (low, high), base_type)
                var_name = expr[1]
                var_info = self.symbol_table.get_var_info(var_name)
                # o tipo final do array_access é o tipo dos elementos, não do array inteiro
                _, _, elem_type = var_info['type']
                return elem_type
            # literal numérico encapsulado
            if op == 'num':
                if isinstance(expr[1], float):
                    return 'real'
                return 'integer'
            # literal string encapsulado
            if op == 'string':
                return 'string'
            # caso 'var' (referência a variável)
            if op == 'var':
                var_info = self.symbol_table.variables.get(expr[1])
                return var_info['type'] if var_info else 'integer'

        # 3) Se for string “simples” → ou literal de string (com caracteres não alfanuméricos)
        if isinstance(expr, str):
            # Verifica se é uma variável conhecida
            var = self.symbol_table.variables.get(expr)
            if var:
                return var['type']
            # Caso contrário, se for literal de string (contém aspas, espaços ou pontuação)
            if ' ' in expr or any(c in expr for c in '.,!?;:()[]{}'):
                return 'string'
            # Senão, assume identificador de inteiro
            return 'integer'

        # 4) Se for número “puro” (Nunca cai aqui, porque já foi capturado por isinstance(int/float)?)
        return 'integer'  # fallback

    def translate_readln(self, stmt):
        """Translate readln para variáveis simples."""
        # stmt = ('readln', var_name)
        var_name = stmt[1]
        var_info = self.symbol_table.get_var_info(var_name)

        # Gerar READ
        self.vm_code.append("READ")

        # Converter string lida para tipo correto
        var_type = var_info['type']
        if var_type == 'integer':
            self.vm_code.append("ATOI")
        elif var_type == 'real':
            self.vm_code.append("ATOF")
        elif var_type == 'boolean':
            self.vm_code.append("ATOI")

        # Armazenar em var
        self.vm_code.append(f"STOREG {var_info['address']}")

    def translate_readln_array(self, stmt):
        """Translate readln para elemento de array."""
        # stmt = ('readln_array', array_name, index_exp)
        array_name = stmt[1]
        index_exp = stmt[2]

        if array_name not in self.symbol_table.variables:
            raise ValueError(f"Undefined array: {array_name}")

        array_info = self.symbol_table.get_var_info(array_name)
        # Endereço base do array
        self.vm_code.append(f"PUSHG {array_info['address']}")

        # Índice (semelhante ao translate_array_access)
        if isinstance(index_exp, tuple) and index_exp[0] == 'var':
            _, var = index_exp
            var_add = self.symbol_table.variables.get(var)['address']
        else:
            var_add = index_exp

        self.vm_code.append(f"PUSHG {var_add}")
        self.vm_code.append("PUSHI 1")
        self.vm_code.append("SUB")

        # Faz leitura em array[index]
        self.vm_code.append("READ")

        # Converte de string para tipo dos elementos
        _, _, elem_type = array_info['type']
        if elem_type == 'integer':
            self.vm_code.append("ATOI")
        elif elem_type == 'real':
            self.vm_code.append("ATOF")
        elif elem_type == 'boolean':
            self.vm_code.append("ATOI")

        self.vm_code.append("STOREN")

    def translate_if(self, stmt):
        """Translate if statement."""
        # stmt = ('if', condition_exp, ('then', then_block), ('else', else_block)?)
        condition = stmt[1]
        then_block = stmt[2][1]
        else_block = stmt[3][1] if stmt[3] else None

        # Gera rótulos únicos
        false_label = self.label_gen.generate('ifFalse')
        end_label = self.label_gen.generate('ifEnd')

        # Avalia condição e empurra 0/1
        self.expr_translator.translate(condition)

        # Se zero, salta para else
        self.vm_code.append(f"JZ {false_label}")

        # Then‐block
        self.translate(then_block)

        if else_block:
            # Salta por cima do else
            self.vm_code.append(f"JUMP {end_label}")

        # Rótulo “else” (se existir)
        self.vm_code.append(f"{false_label}:")

        if else_block:
            self.translate(else_block)
            # Rótulo final
            self.vm_code.append(f"{end_label}:")

    def translate_while(self, stmt):
        """Translate while loop."""
        # stmt = ('while', condition, body)
        condition = stmt[1]
        body = stmt[2]

        start_label = self.label_gen.generate('whileStart')
        end_label = self.label_gen.generate('whileEnd')

        self.vm_code.append(f"{start_label}:")

        # Avalia condição
        self.expr_translator.translate(condition)
        # Se false, sai
        self.vm_code.append(f"JZ {end_label}")

        # Corpo
        self.translate(body)
        # Volta para o início
        self.vm_code.append(f"JUMP {start_label}")

        self.vm_code.append(f"{end_label}:")

    def translate_for(self, stmt):
        """Translate for loop."""
        # stmt = ('for', var_name, start_exp, end_exp, body)
        var_name = stmt[1]
        start_exp = stmt[2]
        end_exp = stmt[3]
        body = stmt[4]

        # Garante que a variável existe
        if var_name not in self.symbol_table.variables:
            self.symbol_table.allocate_var(var_name, 'integer')
        var_info = self.symbol_table.get_var_info(var_name)

        # Avalia e armazena _inicial_
        self.expr_translator.translate(start_exp)
        self.vm_code.append(f"STOREG {var_info['address']}")

        start_label = self.label_gen.generate('forStart')
        end_label = self.label_gen.generate('forEnd')

        self.vm_code.append(f"{start_label}:")

        # Carrega var atual
        self.vm_code.append(f"PUSHG {var_info['address']}")
        # Avalia condição “to” (Sempre “to” no vosso parser)
        self.expr_translator.translate(end_exp)
        # Se var > end, sai (usamos INFEQ = var <= end)
        self.vm_code.append("INFEQ")
        self.vm_code.append(f"JZ {end_label}")

        # Corpo do laço
        self.translate(body)

        # Incrementa var
        self.vm_code.append(f"PUSHG {var_info['address']}")
        self.vm_code.append("PUSHI 1")
        self.vm_code.append("ADD")
        self.vm_code.append(f"STOREG {var_info['address']}")

        self.vm_code.append(f"JUMP {start_label}")
        self.vm_code.append(f"{end_label}:")

    def translate_compound(self, stmt):
        """Translate compound statement (várias instruções)."""
        # stmt = ('compound', [sub_stmt1, sub_stmt2, ...])
        for sub_stmt in stmt[1]:
            self.translate(sub_stmt)

    def translate(self, stmt):
        """Main statement dispatcher."""
        if not isinstance(stmt, tuple):
            # Tratamento de writeln sem argumentos (token único)
            if stmt == 'writeln':
                op = stmt
            else:
                return
        else:
            op = stmt[0]

        translation_map = {
            'assign': self.translate_assignment,
            'write': self.translate_write,
            'writeln': self.translate_writeln,
            'readln': self.translate_readln,
            'readln_array': self.translate_readln_array,
            'if': self.translate_if,
            'while': self.translate_while,
            'for': self.translate_for,
            'compound': self.translate_compound
        }

        translator = translation_map.get(op)
        if translator:
            translator(stmt)
        else:
            print(f"Unsupported statement type: {op}")


class Translator:
    """Main translator class."""

    def __init__(self):
        self.vm_code = []
        self.symbol_table = SymbolTable()
        self.label_gen = LabelGenerator()

    def translate_declarations(self, declarations):
        """Process variable declarations (empurra valor inicial e aloca)."""
        if declarations and declarations[0] == 'var_decls':
            for decl in declarations[1]:
                var_names = decl[1]
                var_type = decl[2]

                for var_name in var_names:
                    if var_type == 'integer':
                        # inicializa inteiro com 0
                        self.vm_code.append("PUSHI 0")
                    elif var_type == 'real':
                        # inicializa real com 0.0
                        self.vm_code.append("PUSHF 0.0")
                    elif var_type == 'string':
                        # inicializa string vazia
                        self.vm_code.append("PUSHS \"\"")
                    elif var_type == 'boolean':
                        # inicializa booleano como inteiro 0
                        self.vm_code.append("PUSHI 0")
                    elif isinstance(var_type, tuple) and var_type[0] == 'array':
                        # array [low..high] → aloca “size” posições
                        low, high = var_type[1]
                        size = high - low + 1
                        self.vm_code.append(f"PUSHI {size}")
                        self.vm_code.append("ALLOCN")
                    # Depois, registra na tabela de símbolos:
                    self.symbol_table.allocate_var(var_name, var_type)

    def translate_program(self, ast):
        """Translate entire Pascal program AST to VM code."""
        self.vm_code = []

        # AST: ('program', program_name, code)
        program_name = ast[1]
        code_block = ast[2]

        # Se há bloco “code” (declarações + corpo)
        if code_block[0] == 'code':
            declarations = code_block[1]
            self.translate_declarations(declarations)

            # Início do programa na VM
            self.vm_code.append("START")

            # Cria tradutores de expressão e statement
            expr_translator = ExpressionTranslator(
                self.symbol_table,
                self.vm_code
            )
            stmt_translator = StatementTranslator(
                self.symbol_table,
                self.vm_code,
                self.label_gen,
                expr_translator
            )

            # Traduz o corpo principal
            main_body = code_block[2]
            stmt_translator.translate(main_body)

        # Fim do programa na VM
        self.vm_code.append("STOP")
        return self.vm_code
