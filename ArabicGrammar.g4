/**
 * ANTLR4 Grammar for the Arabic Programming Language
 Based on the rules provided by Dr. Khalid M.
 * Al-Kahsah.
 This grammar defines the structure of the language, from the overall program
 down
 * to
 expressions and individual tokens.
 By Engineer : Tareq Al-Omari
 */
grammar ArabicGrammar;

// ------------------------------------------------------------------ # Parser Rules
// ------------------------------------------------------------------

program: PROGRAM ID SEMICOLON block DOT; // بداية البرنامج

block: definitions_part instructions_list;
definitions_part:
	constants_definition? types_definition? variables_definition? procedures_definition?;

// --- Definitions Sections ---

constants_definition: CONST (constant_def)+;

constant_def: ID EQUALS constant_value SEMICOLON;

types_definition: TYPE (type_def)+;

type_def: ID EQUALS composite_type SEMICOLON;

variables_definition: VARIABLE (variable_def)+;

variable_def: variables_group SEMICOLON;

procedures_definition: (procedure_def)+;

procedure_def: procedure_header procedure_block SEMICOLON;

// --- Composite Types & Structures ---

composite_type: list_type | record_type;

list_type:
	LIST L_SQUARE_BRACKET INTEGER R_SQUARE_BRACKET FROM data_type;

record_type: RECORD L_CURLY_BRACE fields_list R_CURLY_BRACE;

fields_list: field_def (SEMICOLON field_def)*;

field_def: ID (COMMA ID)* COLON data_type;

variables_group: ID (COMMA ID)* COLON data_type;

// --- Procedure Declaration ---

procedure_header:
	PROCEDURE ID L_PAREN formal_params_list? R_PAREN SEMICOLON;

procedure_block: block;

formal_params_list: param_def (SEMICOLON param_def)*;

param_def: (BY_VALUE | BY_REFERENCE)? variables_group;

// --- Data Types ---

data_type:
	DT_INTEGER
	| DT_REAL
	| DT_LOGICAL
	| DT_CHAR
	| DT_STRING
	| ID;

// ------------------------------------------------------------------ # Statements
// ------------------------------------------------------------------

instructions_list:
	L_CURLY_BRACE instruction (SEMICOLON instruction)* R_CURLY_BRACE;

instruction:
	assignment_statement
	| input_statement
	| output_statement
	| call_statement
	| conditional_statement
	| loop_statement
	| instructions_list
	|; // empty statement

assignment_statement: variable_access EQUALS expression;

input_statement: READ L_PAREN variable_access R_PAREN;

output_statement: PRINT L_PAREN print_list R_PAREN;

call_statement: ID L_PAREN actual_params_list? R_PAREN;

print_list: print_item (COMMA print_item)*;

print_item: variable_access | literal_value;

actual_params_list: actual_param (COMMA actual_param)*;

actual_param: expression | variable_access;

// --- Conditional and Loop Statements ---

conditional_statement:
	IF L_PAREN condition R_PAREN THEN instruction (
		ELSE IF L_PAREN condition R_PAREN THEN instruction
	)* (ELSE instruction)?;

condition: expression;

loop_statement:
	for_loop_statement
	| while_loop_statement
	| repeat_until_statement;

for_loop_statement:
	FOR L_PAREN iteration_range R_PAREN instruction;

iteration_range:
	ID EQUALS expression TO expression (STEP expression)?;

while_loop_statement:
	WHILE L_PAREN condition R_PAREN CONTINUE instruction;

repeat_until_statement:
	REPEAT instruction UNTIL L_PAREN condition R_PAREN;

// ------------------------------------------------------------------ # Expressions
// ------------------------------------------------------------------

expression:
	simple_expression (relational_op simple_expression)?;

simple_expression: sign? term (add_op term)*;

term: factor (mul_op factor)*;

factor:
	variable_access
	| constant_value
	| L_PAREN expression R_PAREN
	| NOT factor;

variable_access: ID selector?;

selector: indexed_selector | field_selector;

indexed_selector: L_SQUARE_BRACKET expression R_SQUARE_BRACKET;

field_selector: DOT ID;

constant_value:
	numeric_value
	| literal_value
	| logical_value
	| ID;

numeric_value: REAL_NUMBER | INTEGER;

literal_value: STRING_LITERAL | CHAR_LITERAL;

logical_value: TRUE | FALSE;

relational_op: GT | LT | GTE | LTE | EQUALS_OP | NOT_EQUALS_OP;

sign: PLUS | MINUS;

add_op: PLUS | MINUS | OR;

mul_op: MULT | DIV | INT_DIV | MOD | AND;

// ------------------------------------------------------------------ # Lexer Rules
// ------------------------------------------------------------------

PROGRAM: 'برنامج';
CONST: 'ثابت';
TYPE: 'نوع';
VARIABLE: 'متغير';
PROCEDURE: 'اجراء';
LIST: 'قائمة';
FROM: 'من';
RECORD: 'سجل';
BY_VALUE: 'بالقيمة';
BY_REFERENCE: 'بالمرجع';
IF: 'اذا';
THEN: 'فان';
ELSE: 'والا';
FOR: 'كرر';
TO: 'الى';
STEP: 'اضف';
WHILE: 'طالما';
CONTINUE: 'استمر';
REPEAT: 'اعد';
UNTIL: 'حتى';
READ: 'اقرا';
PRINT: 'اطبع';
TRUE: 'صح';
FALSE: 'خطأ';

DT_INTEGER: 'صحيح';
DT_REAL: 'حقيقي';
DT_LOGICAL: 'منطقي';
DT_CHAR: 'حرفي';
DT_STRING: 'خيط_رمزي';

L_PAREN: '(';
R_PAREN: ')';
L_SQUARE_BRACKET: '[';
R_SQUARE_BRACKET: ']';
L_CURLY_BRACE: '{';
R_CURLY_BRACE: '}';
COMMA: '،';
SEMICOLON: '؛';
COLON: ':';
DOT: '.';
EQUALS: '=';

PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';
INT_DIV: '\\';
MOD: '%';
POWER: '^';

AND: '&&';
OR: '||';
NOT: '!';
EQUALS_OP: '==';
NOT_EQUALS_OP: '=!';
GTE: '>=';
LTE: '<=';
GT: '>';
LT: '<';

ID: ARABIC_LETTER (ARABIC_LETTER | DIGIT | '_')*;
REAL_NUMBER: INTEGER '.' INTEGER;
INTEGER: DIGIT+;
STRING_LITERAL: '"' (~["\r\n])* '"';
CHAR_LITERAL: '\'' . '\'';

fragment ARABIC_LETTER: [\u0621-\u064A];
fragment DIGIT: [0-9];

// اضف هذا السطر لتعريف التعليقات
COMMENT: '--' ~[\r\n]* -> skip;

WS: [ \t\r\n]+ -> skip;