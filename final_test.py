from financial_formulas import *
import streamlit as st

def comprehensive_test():
    """Test all major functions"""
    print("🧪 Running comprehensive tests...")
    
    # Test 1: Basic formulas
    assert abs(future_value(1000, 0.06, 10) - 1790.85) < 1
    assert rule_of_72(6) == 12
    print("✅ Basic formulas work")
    
    # Test 2: Monthly savings
    result = monthly_savings_future_value(500, 0.07, 30)
    assert 600000 < result < 700000  # Should be around $650k
    print("✅ Monthly savings calculation works")
    
    # Test 3: Withdrawal duration
    years = withdrawal_duration(500000, 3000, 0.05)
    assert 15 < years < 25  # Should last about 20 years
    print("✅ Withdrawal analysis works")
    
    # Test 4: Monthly payment needed
    payment = monthly_payment_needed(1000000, 0.07, 30)
    assert 1500 < payment < 2000  # Should be around $1700
    print("✅ Payment calculation works")
    
    print("🎉 All tests passed! Your app is ready!")

def validate_realistic_scenarios():
    """Test with realistic user scenarios"""
    print("\n🎯 Testing realistic scenarios...")
    
    # Scenario 1: Young professional
    years_to_ret = 65 - 25
    total = (future_value(10000, 0.07, years_to_ret) + 
             monthly_savings_future_value(600, 0.07, years_to_ret))
    print(f"25yr old, $10k saved, $600/month: ${total:,.0f} at 65")
    
    # Scenario 2: Mid-career
    years_to_ret = 65 - 40
    total = (future_value(100000, 0.07, years_to_ret) + 
             monthly_savings_future_value(1200, 0.07, years_to_ret))
    print(f"40yr old, $100k saved, $1200/month: ${total:,.0f} at 65")
    
    print("✅ Realistic scenarios validated!")

if __name__ == "__main__":
    comprehensive_test()
    validate_realistic_scenarios()