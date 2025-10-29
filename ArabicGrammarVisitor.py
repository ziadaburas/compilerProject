# Generated from ArabicGrammar.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .ArabicGrammarParser import ArabicGrammarParser
else:
    from ArabicGrammarParser import ArabicGrammarParser

# This class defines a complete generic visitor for a parse tree produced by ArabicGrammarParser.

class ArabicGrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ArabicGrammarParser#program.
    def visitProgram(self, ctx:ArabicGrammarParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#block.
    def visitBlock(self, ctx:ArabicGrammarParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#definitions_part.
    def visitDefinitions_part(self, ctx:ArabicGrammarParser.Definitions_partContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#constants_definition.
    def visitConstants_definition(self, ctx:ArabicGrammarParser.Constants_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#constant_def.
    def visitConstant_def(self, ctx:ArabicGrammarParser.Constant_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#types_definition.
    def visitTypes_definition(self, ctx:ArabicGrammarParser.Types_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#type_def.
    def visitType_def(self, ctx:ArabicGrammarParser.Type_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#variables_definition.
    def visitVariables_definition(self, ctx:ArabicGrammarParser.Variables_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#variable_def.
    def visitVariable_def(self, ctx:ArabicGrammarParser.Variable_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#procedures_definition.
    def visitProcedures_definition(self, ctx:ArabicGrammarParser.Procedures_definitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#procedure_def.
    def visitProcedure_def(self, ctx:ArabicGrammarParser.Procedure_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#composite_type.
    def visitComposite_type(self, ctx:ArabicGrammarParser.Composite_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#list_type.
    def visitList_type(self, ctx:ArabicGrammarParser.List_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#record_type.
    def visitRecord_type(self, ctx:ArabicGrammarParser.Record_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#fields_list.
    def visitFields_list(self, ctx:ArabicGrammarParser.Fields_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#field_def.
    def visitField_def(self, ctx:ArabicGrammarParser.Field_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#variables_group.
    def visitVariables_group(self, ctx:ArabicGrammarParser.Variables_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#procedure_header.
    def visitProcedure_header(self, ctx:ArabicGrammarParser.Procedure_headerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#procedure_block.
    def visitProcedure_block(self, ctx:ArabicGrammarParser.Procedure_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#formal_params_list.
    def visitFormal_params_list(self, ctx:ArabicGrammarParser.Formal_params_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#param_def.
    def visitParam_def(self, ctx:ArabicGrammarParser.Param_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#data_type.
    def visitData_type(self, ctx:ArabicGrammarParser.Data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#instructions_list.
    def visitInstructions_list(self, ctx:ArabicGrammarParser.Instructions_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#instruction.
    def visitInstruction(self, ctx:ArabicGrammarParser.InstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#assignment_statement.
    def visitAssignment_statement(self, ctx:ArabicGrammarParser.Assignment_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#input_statement.
    def visitInput_statement(self, ctx:ArabicGrammarParser.Input_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#output_statement.
    def visitOutput_statement(self, ctx:ArabicGrammarParser.Output_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#call_statement.
    def visitCall_statement(self, ctx:ArabicGrammarParser.Call_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#print_list.
    def visitPrint_list(self, ctx:ArabicGrammarParser.Print_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#print_item.
    def visitPrint_item(self, ctx:ArabicGrammarParser.Print_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#actual_params_list.
    def visitActual_params_list(self, ctx:ArabicGrammarParser.Actual_params_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#actual_param.
    def visitActual_param(self, ctx:ArabicGrammarParser.Actual_paramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#conditional_statement.
    def visitConditional_statement(self, ctx:ArabicGrammarParser.Conditional_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#condition.
    def visitCondition(self, ctx:ArabicGrammarParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#loop_statement.
    def visitLoop_statement(self, ctx:ArabicGrammarParser.Loop_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#for_loop_statement.
    def visitFor_loop_statement(self, ctx:ArabicGrammarParser.For_loop_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#iteration_range.
    def visitIteration_range(self, ctx:ArabicGrammarParser.Iteration_rangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#while_loop_statement.
    def visitWhile_loop_statement(self, ctx:ArabicGrammarParser.While_loop_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#repeat_until_statement.
    def visitRepeat_until_statement(self, ctx:ArabicGrammarParser.Repeat_until_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#expression.
    def visitExpression(self, ctx:ArabicGrammarParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#simple_expression.
    def visitSimple_expression(self, ctx:ArabicGrammarParser.Simple_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#term.
    def visitTerm(self, ctx:ArabicGrammarParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#factor.
    def visitFactor(self, ctx:ArabicGrammarParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#variable_access.
    def visitVariable_access(self, ctx:ArabicGrammarParser.Variable_accessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#selector.
    def visitSelector(self, ctx:ArabicGrammarParser.SelectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#indexed_selector.
    def visitIndexed_selector(self, ctx:ArabicGrammarParser.Indexed_selectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#field_selector.
    def visitField_selector(self, ctx:ArabicGrammarParser.Field_selectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#constant_value.
    def visitConstant_value(self, ctx:ArabicGrammarParser.Constant_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#numeric_value.
    def visitNumeric_value(self, ctx:ArabicGrammarParser.Numeric_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#literal_value.
    def visitLiteral_value(self, ctx:ArabicGrammarParser.Literal_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#logical_value.
    def visitLogical_value(self, ctx:ArabicGrammarParser.Logical_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#relational_op.
    def visitRelational_op(self, ctx:ArabicGrammarParser.Relational_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#sign.
    def visitSign(self, ctx:ArabicGrammarParser.SignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#add_op.
    def visitAdd_op(self, ctx:ArabicGrammarParser.Add_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ArabicGrammarParser#mul_op.
    def visitMul_op(self, ctx:ArabicGrammarParser.Mul_opContext):
        return self.visitChildren(ctx)



del ArabicGrammarParser