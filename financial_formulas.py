import math

def future_value(present_value, annual_rate, years):
    """Calculate future value: FV = PV × (1 + r)^n"""
    return present_value * (1 + annual_rate) ** years

def present_value(future_value, annual_rate, years):
    """Calculate present value: PV = FV ÷ (1 + r)^n"""
    return future_value / (1 + annual_rate) ** years

def future_value_annuity(payment, annual_rate, years):
    """Future value of regular payments"""
    if annual_rate == 0:
        return payment * years
    return payment * ((1 + annual_rate) ** years - 1) / annual_rate

def monthly_savings_future_value(monthly_payment, annual_rate, years):
    """Calculate future value of monthly savings"""
    monthly_rate = (1 + annual_rate) ** (1/12) - 1
    months = years * 12
    if monthly_rate == 0:
        return monthly_payment * months
    return monthly_payment * ((1 + monthly_rate) ** months - 1) / monthly_rate

def calculate_retirement_needs(monthly_expenses, years_in_retirement, annual_rate):
    """Calculate how much needed for retirement"""
    annual_expenses = monthly_expenses * 12
    return present_value(annual_expenses * years_in_retirement, annual_rate, 0)

def rule_of_72(annual_rate_percent):
    """Years to double money"""
    return 72 / annual_rate_percent

def monthly_payment_needed(target_amount, annual_rate, years):
    """How much to save monthly to reach target"""
    monthly_rate = (1 + annual_rate) ** (1/12) - 1
    months = years * 12
    if monthly_rate == 0:
        return target_amount / months
    return target_amount * monthly_rate / ((1 + monthly_rate) ** months - 1)

def withdrawal_duration(starting_amount, monthly_withdrawal, annual_rate):
    """How long money will last with withdrawals"""
    if annual_rate == 0:
        return starting_amount / monthly_withdrawal / 12
    
    monthly_rate = (1 + annual_rate) ** (1/12) - 1
    if monthly_withdrawal <= starting_amount * monthly_rate:
        return float('inf')  # Money lasts forever
    
    months = -math.log(1 - (starting_amount * monthly_rate / monthly_withdrawal)) / math.log(1 + monthly_rate)
    return months / 12


def calculate_nper(rate, payment, present_value, future_value=0):
    """
    Excel-style NPER function
    Calculate number of periods for an investment based on periodic payments
    """
    if rate == 0:
        return -(future_value + present_value) / payment
    
    import math
    try:
        numerator = math.log((-future_value + payment / rate) / (present_value + payment / rate))
        denominator = math.log(1 + rate)
        return numerator / denominator
    except (ValueError, ZeroDivisionError):
        return float('inf')
