from financial_formulas import *

def test_basics():
    # Test 1: $1000 at 6% for 10 years = ~$1791
    result = future_value(1000, 0.06, 10)
    print(f"$1000 at 6% for 10 years: ${result:.2f}")
    assert 1790 < result < 1792, "Future value test failed"
    
    # Test 2: Rule of 72
    years = rule_of_72(6)
    print(f"Money doubles in {years} years at 6%")
    assert years == 12, "Rule of 72 test failed"
    
    # Test 3: Monthly savings
    result = monthly_savings_future_value(500, 0.07, 30)
    print(f"$500/month for 30 years at 7%: ${result:.2f}")
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_basics()