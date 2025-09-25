from utils.expense_calculator import Calculator
from typing import List
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools with structured schemas"""
        
        class EstimateHotelCostInput(BaseModel):
            price_per_night: float = Field(..., description="Price per night of hotel")
            total_days: float = Field(..., description="Number of nights to stay")

        def estimate_total_hotel_cost(price_per_night: float, total_days: float) -> float:
            return self.calculator.multiply(float(price_per_night), float(total_days))

        class CalculateTotalExpenseInput(BaseModel):
            costs: List[float] = Field(..., description="List of costs to sum")

        def calculate_total_expense(*costs: float) -> float:
            return self.calculator.calculate_total(*costs)

        class CalculateDailyBudgetInput(BaseModel):
            total_cost: float
            days: int

        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            return self.calculator.calculate_daily_budget(total_cost, days)

        return [
            StructuredTool.from_function(
                func=estimate_total_hotel_cost,
                args_schema=EstimateHotelCostInput,
                description="Calculate total hotel cost"
            ),
            StructuredTool.from_function(
                func=calculate_total_expense,
                args_schema=CalculateTotalExpenseInput,
                description="Calculate total trip expense"
            ),
            StructuredTool.from_function(
                func=calculate_daily_expense_budget,
                args_schema=CalculateDailyBudgetInput,
                description="Calculate daily expense budget"
            ),
        ]