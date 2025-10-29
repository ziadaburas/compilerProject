# Generated from ArabicGrammar.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .ArabicGrammarParser import ArabicGrammarParser
else:
    from ArabicGrammarParser import ArabicGrammarParser

# This class defines a complete listener for a parse tree produced by ArabicGrammarParser.
class ArabicGrammarListener(ParseTreeListener):

    # Enter a parse tree produced by ArabicGrammarParser#program.
    def enterProgram(self, ctx:ArabicGrammarParser.ProgramContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#program.
    def exitProgram(self, ctx:ArabicGrammarParser.ProgramContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#block.
    def enterBlock(self, ctx:ArabicGrammarParser.BlockContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#block.
    def exitBlock(self, ctx:ArabicGrammarParser.BlockContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#definitions_part.
    def enterDefinitions_part(self, ctx:ArabicGrammarParser.Definitions_partContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#definitions_part.
    def exitDefinitions_part(self, ctx:ArabicGrammarParser.Definitions_partContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#constants_definition.
    def enterConstants_definition(self, ctx:ArabicGrammarParser.Constants_definitionContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#constants_definition.
    def exitConstants_definition(self, ctx:ArabicGrammarParser.Constants_definitionContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#constant_def.
    def enterConstant_def(self, ctx:ArabicGrammarParser.Constant_defContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#constant_def.
    def exitConstant_def(self, ctx:ArabicGrammarParser.Constant_defContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#types_definition.
    def enterTypes_definition(self, ctx:ArabicGrammarParser.Types_definitionContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#types_definition.
    def exitTypes_definition(self, ctx:ArabicGrammarParser.Types_definitionContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#type_def.
    def enterType_def(self, ctx:ArabicGrammarParser.Type_defContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#type_def.
    def exitType_def(self, ctx:ArabicGrammarParser.Type_defContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#variables_definition.
    def enterVariables_definition(self, ctx:ArabicGrammarParser.Variables_definitionContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#variables_definition.
    def exitVariables_definition(self, ctx:ArabicGrammarParser.Variables_definitionContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#variable_def.
    def enterVariable_def(self, ctx:ArabicGrammarParser.Variable_defContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#variable_def.
    def exitVariable_def(self, ctx:ArabicGrammarParser.Variable_defContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#procedures_definition.
    def enterProcedures_definition(self, ctx:ArabicGrammarParser.Procedures_definitionContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#procedures_definition.
    def exitProcedures_definition(self, ctx:ArabicGrammarParser.Procedures_definitionContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#procedure_def.
    def enterProcedure_def(self, ctx:ArabicGrammarParser.Procedure_defContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#procedure_def.
    def exitProcedure_def(self, ctx:ArabicGrammarParser.Procedure_defContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#composite_type.
    def enterComposite_type(self, ctx:ArabicGrammarParser.Composite_typeContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#composite_type.
    def exitComposite_type(self, ctx:ArabicGrammarParser.Composite_typeContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#list_type.
    def enterList_type(self, ctx:ArabicGrammarParser.List_typeContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#list_type.
    def exitList_type(self, ctx:ArabicGrammarParser.List_typeContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#record_type.
    def enterRecord_type(self, ctx:ArabicGrammarParser.Record_typeContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#record_type.
    def exitRecord_type(self, ctx:ArabicGrammarParser.Record_typeContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#fields_list.
    def enterFields_list(self, ctx:ArabicGrammarParser.Fields_listContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#fields_list.
    def exitFields_list(self, ctx:ArabicGrammarParser.Fields_listContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#field_def.
    def enterField_def(self, ctx:ArabicGrammarParser.Field_defContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#field_def.
    def exitField_def(self, ctx:ArabicGrammarParser.Field_defContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#variables_group.
    def enterVariables_group(self, ctx:ArabicGrammarParser.Variables_groupContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#variables_group.
    def exitVariables_group(self, ctx:ArabicGrammarParser.Variables_groupContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#procedure_header.
    def enterProcedure_header(self, ctx:ArabicGrammarParser.Procedure_headerContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#procedure_header.
    def exitProcedure_header(self, ctx:ArabicGrammarParser.Procedure_headerContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#procedure_block.
    def enterProcedure_block(self, ctx:ArabicGrammarParser.Procedure_blockContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#procedure_block.
    def exitProcedure_block(self, ctx:ArabicGrammarParser.Procedure_blockContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#formal_params_list.
    def enterFormal_params_list(self, ctx:ArabicGrammarParser.Formal_params_listContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#formal_params_list.
    def exitFormal_params_list(self, ctx:ArabicGrammarParser.Formal_params_listContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#param_def.
    def enterParam_def(self, ctx:ArabicGrammarParser.Param_defContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#param_def.
    def exitParam_def(self, ctx:ArabicGrammarParser.Param_defContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#data_type.
    def enterData_type(self, ctx:ArabicGrammarParser.Data_typeContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#data_type.
    def exitData_type(self, ctx:ArabicGrammarParser.Data_typeContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#instructions_list.
    def enterInstructions_list(self, ctx:ArabicGrammarParser.Instructions_listContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#instructions_list.
    def exitInstructions_list(self, ctx:ArabicGrammarParser.Instructions_listContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#instruction.
    def enterInstruction(self, ctx:ArabicGrammarParser.InstructionContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#instruction.
    def exitInstruction(self, ctx:ArabicGrammarParser.InstructionContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#assignment_statement.
    def enterAssignment_statement(self, ctx:ArabicGrammarParser.Assignment_statementContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#assignment_statement.
    def exitAssignment_statement(self, ctx:ArabicGrammarParser.Assignment_statementContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#input_statement.
    def enterInput_statement(self, ctx:ArabicGrammarParser.Input_statementContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#input_statement.
    def exitInput_statement(self, ctx:ArabicGrammarParser.Input_statementContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#output_statement.
    def enterOutput_statement(self, ctx:ArabicGrammarParser.Output_statementContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#output_statement.
    def exitOutput_statement(self, ctx:ArabicGrammarParser.Output_statementContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#call_statement.
    def enterCall_statement(self, ctx:ArabicGrammarParser.Call_statementContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#call_statement.
    def exitCall_statement(self, ctx:ArabicGrammarParser.Call_statementContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#print_list.
    def enterPrint_list(self, ctx:ArabicGrammarParser.Print_listContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#print_list.
    def exitPrint_list(self, ctx:ArabicGrammarParser.Print_listContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#print_item.
    def enterPrint_item(self, ctx:ArabicGrammarParser.Print_itemContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#print_item.
    def exitPrint_item(self, ctx:ArabicGrammarParser.Print_itemContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#actual_params_list.
    def enterActual_params_list(self, ctx:ArabicGrammarParser.Actual_params_listContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#actual_params_list.
    def exitActual_params_list(self, ctx:ArabicGrammarParser.Actual_params_listContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#actual_param.
    def enterActual_param(self, ctx:ArabicGrammarParser.Actual_paramContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#actual_param.
    def exitActual_param(self, ctx:ArabicGrammarParser.Actual_paramContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#conditional_statement.
    def enterConditional_statement(self, ctx:ArabicGrammarParser.Conditional_statementContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#conditional_statement.
    def exitConditional_statement(self, ctx:ArabicGrammarParser.Conditional_statementContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#condition.
    def enterCondition(self, ctx:ArabicGrammarParser.ConditionContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#condition.
    def exitCondition(self, ctx:ArabicGrammarParser.ConditionContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#loop_statement.
    def enterLoop_statement(self, ctx:ArabicGrammarParser.Loop_statementContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#loop_statement.
    def exitLoop_statement(self, ctx:ArabicGrammarParser.Loop_statementContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#for_loop_statement.
    def enterFor_loop_statement(self, ctx:ArabicGrammarParser.For_loop_statementContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#for_loop_statement.
    def exitFor_loop_statement(self, ctx:ArabicGrammarParser.For_loop_statementContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#iteration_range.
    def enterIteration_range(self, ctx:ArabicGrammarParser.Iteration_rangeContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#iteration_range.
    def exitIteration_range(self, ctx:ArabicGrammarParser.Iteration_rangeContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#while_loop_statement.
    def enterWhile_loop_statement(self, ctx:ArabicGrammarParser.While_loop_statementContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#while_loop_statement.
    def exitWhile_loop_statement(self, ctx:ArabicGrammarParser.While_loop_statementContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#repeat_until_statement.
    def enterRepeat_until_statement(self, ctx:ArabicGrammarParser.Repeat_until_statementContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#repeat_until_statement.
    def exitRepeat_until_statement(self, ctx:ArabicGrammarParser.Repeat_until_statementContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#expression.
    def enterExpression(self, ctx:ArabicGrammarParser.ExpressionContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#expression.
    def exitExpression(self, ctx:ArabicGrammarParser.ExpressionContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#simple_expression.
    def enterSimple_expression(self, ctx:ArabicGrammarParser.Simple_expressionContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#simple_expression.
    def exitSimple_expression(self, ctx:ArabicGrammarParser.Simple_expressionContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#term.
    def enterTerm(self, ctx:ArabicGrammarParser.TermContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#term.
    def exitTerm(self, ctx:ArabicGrammarParser.TermContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#factor.
    def enterFactor(self, ctx:ArabicGrammarParser.FactorContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#factor.
    def exitFactor(self, ctx:ArabicGrammarParser.FactorContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#variable_access.
    def enterVariable_access(self, ctx:ArabicGrammarParser.Variable_accessContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#variable_access.
    def exitVariable_access(self, ctx:ArabicGrammarParser.Variable_accessContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#selector.
    def enterSelector(self, ctx:ArabicGrammarParser.SelectorContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#selector.
    def exitSelector(self, ctx:ArabicGrammarParser.SelectorContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#indexed_selector.
    def enterIndexed_selector(self, ctx:ArabicGrammarParser.Indexed_selectorContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#indexed_selector.
    def exitIndexed_selector(self, ctx:ArabicGrammarParser.Indexed_selectorContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#field_selector.
    def enterField_selector(self, ctx:ArabicGrammarParser.Field_selectorContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#field_selector.
    def exitField_selector(self, ctx:ArabicGrammarParser.Field_selectorContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#constant_value.
    def enterConstant_value(self, ctx:ArabicGrammarParser.Constant_valueContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#constant_value.
    def exitConstant_value(self, ctx:ArabicGrammarParser.Constant_valueContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#numeric_value.
    def enterNumeric_value(self, ctx:ArabicGrammarParser.Numeric_valueContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#numeric_value.
    def exitNumeric_value(self, ctx:ArabicGrammarParser.Numeric_valueContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#literal_value.
    def enterLiteral_value(self, ctx:ArabicGrammarParser.Literal_valueContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#literal_value.
    def exitLiteral_value(self, ctx:ArabicGrammarParser.Literal_valueContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#logical_value.
    def enterLogical_value(self, ctx:ArabicGrammarParser.Logical_valueContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#logical_value.
    def exitLogical_value(self, ctx:ArabicGrammarParser.Logical_valueContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#relational_op.
    def enterRelational_op(self, ctx:ArabicGrammarParser.Relational_opContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#relational_op.
    def exitRelational_op(self, ctx:ArabicGrammarParser.Relational_opContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#sign.
    def enterSign(self, ctx:ArabicGrammarParser.SignContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#sign.
    def exitSign(self, ctx:ArabicGrammarParser.SignContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#add_op.
    def enterAdd_op(self, ctx:ArabicGrammarParser.Add_opContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#add_op.
    def exitAdd_op(self, ctx:ArabicGrammarParser.Add_opContext):
        pass


    # Enter a parse tree produced by ArabicGrammarParser#mul_op.
    def enterMul_op(self, ctx:ArabicGrammarParser.Mul_opContext):
        pass

    # Exit a parse tree produced by ArabicGrammarParser#mul_op.
    def exitMul_op(self, ctx:ArabicGrammarParser.Mul_opContext):
        pass



del ArabicGrammarParser