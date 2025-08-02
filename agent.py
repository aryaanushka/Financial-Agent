import os
import re
from financial_formulas import *

class FinancialPlanningAgent:
    def __init__(self):
        # Simple agent without LangChain dependency for now
        # We'll focus on the core functionality that matches PDF requirements
        self.responses = [
            "Let me calculate that for you using financial formulas.",
            "Based on your profile, here's what the math shows:",
            "I'll analyze this step-by-step using proven formulas.",
            "Here's my calculation using time-value-of-money principles:",
        ]
    
    def process_question(self, question, user_data, show_work=False):
        """Process natural language financial questions"""
        
        # Extract the calculation based on question type
        if "retire" in question.lower() and "age" in question.lower():
            return self.calculate_retirement_age(question, user_data, show_work)
        
        elif "how long" in question.lower() and "last" in question.lower():
            return self.calculate_money_duration(question, user_data, show_work)
        
        elif "save" in question.lower() and ("month" in question.lower() or "target" in question.lower()):
            return self.calculate_savings_target(question, user_data, show_work)
        
        elif "what if" in question.lower():
            return self.handle_what_if(question, user_data, show_work)
        
        elif "mortgage" in question.lower() and "invest" in question.lower():
            return self.mortgage_vs_invest(question, user_data, show_work)
        
        else:
            return self.general_response(question, user_data)
    
    def calculate_retirement_age(self, question, user_data, show_work):
        """Handle: 'I'm 35, save $1000 a month, expect 6% return—what age can I retire?'"""
        
        # Extract numbers from question if provided, otherwise use user profile
        amounts = re.findall(r'\$?(\d+(?:,\d+)*)', question)
        rates = re.findall(r'(\d+(?:\.\d+)?)\s*%', question)
        
        monthly_savings = user_data.get('monthly_savings', 1000)
        expected_return = user_data.get('expected_return', 0.06)
        current_age = user_data.get('age', 35)
        target_amount = user_data.get('monthly_expenses', 4000) * 12 * 25  # 25 years retirement
        
        if amounts:
            monthly_savings = int(amounts[0].replace(',', ''))
        if rates:
            expected_return = float(rates[0]) / 100
        
        # Calculate years needed
        try:
            years_needed = calculate_nper(
                expected_return / 12,  # Monthly rate
                monthly_savings,
                -user_data.get('current_savings', 0),
                target_amount
            ) / 12  # Convert to years
            
            retirement_age = current_age + years_needed
            
            if show_work:
                return self.format_with_work(
                    f"You can retire at age {retirement_age:.0f}",
                    "NPER Formula",
                    f"Monthly savings: ${monthly_savings:,}",
                    f"Expected return: {expected_return*100:.1f}%",
                    f"Target amount: ${target_amount:,}",
                    f"Years needed: {years_needed:.1f}",
                    f"Retirement age: {current_age} + {years_needed:.1f} = {retirement_age:.0f}"
                )
            
            return f"Based on saving ${monthly_savings:,}/month at {expected_return*100:.1f}% return, you can retire at age {retirement_age:.0f}."
            
        except:
            return "Unable to calculate retirement age with current parameters. You may need to save more or adjust expectations."
    
    def calculate_money_duration(self, question, user_data, show_work):
        """Handle: 'If I'm retired with $400,000 and withdraw $3,000 a month at 5%, how long will it last?'"""
        
        # Extract numbers from question
        amounts = re.findall(r'\$?(\d+(?:,\d+)*)', question)
        rates = re.findall(r'(\d+(?:\.\d+)?)\s*%', question)
        
        starting_amount = 400000
        monthly_withdrawal = 3000
        annual_rate = 0.05
        
        if len(amounts) >= 2:
            starting_amount = int(amounts[0].replace(',', ''))
            monthly_withdrawal = int(amounts[1].replace(',', ''))
        if rates:
            annual_rate = float(rates[0]) / 100
        
        years_will_last = withdrawal_duration(starting_amount, monthly_withdrawal, annual_rate)
        
        if show_work:
            monthly_rate = (1 + annual_rate) ** (1/12) - 1
            return self.format_with_work(
                f"Your money will last {years_will_last:.1f} years",
                "Withdrawal Duration Formula",
                f"Starting amount: ${starting_amount:,}",
                f"Monthly withdrawal: ${monthly_withdrawal:,}",
                f"Annual return: {annual_rate*100:.1f}%",
                f"Monthly return: {monthly_rate*100:.3f}%",
                f"Duration: {years_will_last:.1f} years"
            )
        
        if years_will_last == float('inf'):
            return f"Great news! ${starting_amount:,} will last forever with ${monthly_withdrawal:,}/month withdrawals at {annual_rate*100:.1f}% return."
        else:
            return f"${starting_amount:,} will last {years_will_last:.1f} years with ${monthly_withdrawal:,}/month withdrawals at {annual_rate*100:.1f}% return."
    
    def calculate_savings_target(self, question, user_data, show_work):
        """Handle: 'How much must I save monthly to reach $1 million in 25 years?'"""
        
        # Extract target amount and years
        amounts = re.findall(r'\$?(\d+(?:,\d+)*(?:\s*(?:million|k))?)', question.lower())
        years_match = re.findall(r'(\d+)\s*years?', question)
        
        target_amount = 1000000
        years = 25
        annual_rate = user_data.get('expected_return', 0.07)
        
        if amounts:
            amount_str = amounts[0].replace(',', '').replace('$', '').strip()
            if 'million' in amount_str:
                target_amount = float(amount_str.replace('million', '').strip()) * 1000000
            elif 'k' in amount_str:
                target_amount = float(amount_str.replace('k', '').strip()) * 1000
            else:
                target_amount = float(amount_str)
        
        if years_match:
            years = int(years_match[0])
        
        monthly_payment = monthly_payment_needed(target_amount, annual_rate, years)
        
        if show_work:
            return self.format_with_work(
                f"You need to save ${monthly_payment:,.0f} per month",
                "Payment (PMT) Formula",
                f"Target amount: ${target_amount:,}",
                f"Time period: {years} years",
                f"Expected return: {annual_rate*100:.1f}%",
                f"Required monthly payment: ${monthly_payment:,.0f}"
            )
        
        return f"To reach ${target_amount:,} in {years} years at {annual_rate*100:.1f}% return, save ${monthly_payment:,.0f} per month."
    
    def handle_what_if(self, question, user_data, show_work):
        """Handle what-if scenarios like inflation questions"""
        
        if "inflation" in question.lower():
            # Extract inflation rate
            rates = re.findall(r'(\d+(?:\.\d+)?)\s*%', question)
            inflation_rate = float(rates[0]) / 100 if rates else 0.03
            
            # Calculate impact on retirement needs
            years_to_retirement = user_data.get('retirement_age', 65) - user_data.get('age', 30)
            current_expenses = user_data.get('monthly_expenses', 4000) * 12
            future_expenses = current_expenses * (1 + inflation_rate) ** years_to_retirement
            
            if show_work:
                return self.format_with_work(
                    f"With {inflation_rate*100:.1f}% inflation, you'll need ${future_expenses:,.0f}/year",
                    "Future Value with Inflation",
                    f"Current annual expenses: ${current_expenses:,}",
                    f"Inflation rate: {inflation_rate*100:.1f}%",
                    f"Years to retirement: {years_to_retirement}",
                    f"Formula: FV = PV × (1 + inflation)^years",
                    f"Future expenses: ${current_expenses:,} × (1.{inflation_rate*100:02.0f})^{years_to_retirement} = ${future_expenses:,.0f}"
                )
            
            return f"With {inflation_rate*100:.1f}% inflation, your current ${current_expenses:,}/year expenses will become ${future_expenses:,.0f}/year by retirement."
        
        return "Please specify what scenario you'd like to analyze."
    
    def mortgage_vs_invest(self, question, user_data, show_work):
        """Handle: 'Is it smarter to pay down my 3% mortgage or invest at 7%?'"""
        
        rates = re.findall(r'(\d+(?:\.\d+)?)\s*%', question)
        mortgage_rate = float(rates[0]) / 100 if len(rates) >= 1 else 0.03
        invest_rate = float(rates[1]) / 100 if len(rates) >= 2 else 0.07
        
        difference = invest_rate - mortgage_rate
        
        if show_work:
            return self.format_with_work(
                f"Invest! You'll earn {difference*100:.1f}% more by investing",
                "Opportunity Cost Analysis",
                f"Mortgage rate: {mortgage_rate*100:.1f}%",
                f"Investment return: {invest_rate*100:.1f}%",
                f"Net benefit: {invest_rate*100:.1f}% - {mortgage_rate*100:.1f}% = {difference*100:.1f}%",
                "Recommendation: Invest (assuming tax considerations)"
            )
        
        if difference > 0:
            return f"Invest! At {invest_rate*100:.1f}% return vs {mortgage_rate*100:.1f}% mortgage, you'll earn {difference*100:.1f}% more by investing."
        else:
            return f"Pay down mortgage! At {mortgage_rate*100:.1f}% mortgage vs {invest_rate*100:.1f}% return, you'll save {abs(difference)*100:.1f}% by paying down debt."
    
    def general_response(self, question, user_data):
        """Handle general questions"""
        user_profile = f"Age: {user_data.get('age')}, Income: ${user_data.get('annual_income'):,}, Savings: ${user_data.get('monthly_savings'):,}/month"
        
        return f"I can help with specific financial calculations. Try asking about retirement age, savings targets, or withdrawal strategies. Your profile: {user_profile}"
    
    def format_with_work(self, answer, formula_name, *steps):
        """Format response with step-by-step work shown"""
        work_shown = "\n".join([f"• {step}" for step in steps])
        return f"""
**{answer}**

**Formula Used:** {formula_name}

**Step-by-step calculation:**
{work_shown}
        """