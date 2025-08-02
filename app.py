import streamlit as st
import pandas as pd
from financial_formulas import *
import plotly.express as px
import plotly.graph_objects as go
from agent import FinancialPlanningAgent

# Page config
st.set_page_config(page_title="Financial Planning Agent", page_icon="💰", layout="wide")
st.title("💰 Your Personal Financial Planning Agent")
st.markdown("*Get instant retirement planning advice - no AI API needed!*")

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = FinancialPlanningAgent()
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'step' not in st.session_state:
    st.session_state.step = 'input'

def collect_user_info():
    st.subheader("📋 Let's build your financial profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("👤 What's your name?", value="John")
        age = st.number_input("🎂 Current age", min_value=18, max_value=100, value=30)
        annual_income = st.number_input("💵 Annual income ($)", min_value=0, value=60000, step=5000)
        current_savings = st.number_input("🏦 Current savings ($)", min_value=0, value=15000, step=1000)
    
    with col2:
        monthly_savings = st.number_input("📈 Monthly savings ($)", min_value=0, value=800, step=50)
        retirement_age = st.number_input("🏖️ Target retirement age", min_value=age+1, max_value=100, value=65)
        expected_return = st.slider("📊 Expected annual return (%)", min_value=1, max_value=15, value=7)
        monthly_expenses = st.number_input("🛒 Expected monthly expenses in retirement ($)", min_value=0, value=4000, step=100)
    
    if st.button("📊 Analyze My Plan", type="primary"):
        if name:
            st.session_state.user_data = {
                'name': name,
                'age': age,
                'annual_income': annual_income,
                'current_savings': current_savings,
                'monthly_savings': monthly_savings,
                'retirement_age': retirement_age,
                'expected_return': expected_return / 100,
                'monthly_expenses': monthly_expenses
            }
            st.session_state.step = 'analysis'
            st.rerun()

def show_analysis():
    data = st.session_state.user_data
    st.subheader(f"📈 {data['name']}'s Retirement Analysis")
    
    # Core calculations
    years_to_retirement = data['retirement_age'] - data['age']
    years_in_retirement = 25  # Assume 25 years in retirement
    
    # Future value of current savings
    current_savings_future = future_value(
        data['current_savings'], 
        data['expected_return'], 
        years_to_retirement
    )
    
    # Future value of monthly savings
    monthly_savings_future = monthly_savings_future_value(
        data['monthly_savings'],
        data['expected_return'],
        years_to_retirement
    )
    
    total_retirement_fund = current_savings_future + monthly_savings_future
    
    # How much needed for retirement
    retirement_needs = data['monthly_expenses'] * 12 * years_in_retirement
    retirement_needs_pv = present_value(retirement_needs, data['expected_return'], years_to_retirement)
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Years to Retirement", f"{years_to_retirement} years")
    with col2:
        st.metric("Projected Fund", f"${total_retirement_fund:,.0f}")
    with col3:
        st.metric("Retirement Needs", f"${retirement_needs:,.0f}")
    with col4:
        surplus_deficit = total_retirement_fund - retirement_needs_pv
        st.metric("Surplus/Deficit", f"${surplus_deficit:,.0f}", 
                 delta_color="normal" if surplus_deficit >= 0 else "inverse")
    
    # Detailed analysis
    st.subheader("📊 Detailed Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Your Money Will Grow To:")
        st.write(f"• Current ${data['current_savings']:,} → **${current_savings_future:,.0f}**")
        st.write(f"• Monthly ${data['monthly_savings']:,} → **${monthly_savings_future:,.0f}**")
        st.write(f"• **Total at retirement: ${total_retirement_fund:,.0f}**")
        
        # Rule of 72
        doubling_years = rule_of_72(data['expected_return'] * 100)
        st.info(f"💡 At {data['expected_return']*100:.0f}% return, your money doubles every {doubling_years:.1f} years")
    
    with col2:
        st.markdown("### 🎯 Retirement Analysis:")
        monthly_income_from_savings = total_retirement_fund / years_in_retirement / 12
        st.write(f"• You want ${data['monthly_expenses']:,}/month in retirement")
        st.write(f"• Your savings can provide **${monthly_income_from_savings:,.0f}/month**")
        
        if monthly_income_from_savings >= data['monthly_expenses']:
            st.success("✅ You're on track for retirement!")
        else:
            shortfall = data['monthly_expenses'] - monthly_income_from_savings
            st.warning(f"⚠️ Monthly shortfall: ${shortfall:,.0f}")
            
            # Calculate how much more to save
            additional_needed = shortfall * 12 * years_in_retirement
            additional_monthly = monthly_payment_needed(additional_needed, data['expected_return'], years_to_retirement)
            st.write(f"💡 Save ${additional_monthly:.0f} more per month to close the gap")
             
            st.markdown("---")
            st.subheader("📈 Visual Analysis")
    
    # Growth chart
    fig = create_growth_chart(data)
    st.plotly_chart(fig, use_container_width=True)
    
    # Scenarios table
    st.subheader("🎯 Compare Scenarios")
    scenarios_df = retirement_scenarios_table(data)
    st.dataframe(scenarios_df, use_container_width=True)

           

def handle_questions():
    st.subheader("❓ Ask Questions About Your Plan")
    
    # Predefined question buttons
    st.markdown("**Quick Questions:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("What if I save $200 more?"):
            show_what_if_savings(200)
    
    with col2:
        if st.button("What if I retire 2 years later?"):
            show_what_if_retirement_age(2)
    
    with col3:
        if st.button("How long will $500k last?"):
            show_withdrawal_analysis(500000, 4000)
    
    # Custom question input
    st.markdown("**Custom Analysis:**")
    question_type = st.selectbox("What do you want to analyze?", [
        "Extra monthly savings",
        "Different retirement age", 
        "Withdrawal analysis",
        "Different return rate"
    ])
    
    if question_type == "Extra monthly savings":
        extra = st.number_input("Extra monthly savings ($)", min_value=0, value=200, step=50)
        if st.button("Calculate Impact"):
            show_what_if_savings(extra)
    
    elif question_type == "Different retirement age":
        age_change = st.number_input("Years later (+) or earlier (-)", value=0, step=1)
        if st.button("Calculate Impact"):
            show_what_if_retirement_age(age_change)
    
    elif question_type == "Withdrawal analysis":
        amount = st.number_input("Starting amount ($)", min_value=0, value=500000, step=10000)
        withdrawal = st.number_input("Monthly withdrawal ($)", min_value=0, value=4000, step=100)
        if st.button("Calculate Duration"):
            show_withdrawal_analysis(amount, withdrawal)
    
    elif question_type == "Different return rate":
        new_rate = st.slider("New expected return (%)", min_value=1, max_value=15, value=8)
        if st.button("Calculate Impact"):
            show_what_if_return_rate(new_rate / 100)

def show_what_if_savings(extra_amount):
    data = st.session_state.user_data
    years_to_retirement = data['retirement_age'] - data['age']
    
    # Current plan
    current_future = monthly_savings_future_value(
        data['monthly_savings'], data['expected_return'], years_to_retirement
    )
    
    # New plan
    new_monthly = data['monthly_savings'] + extra_amount
    new_future = monthly_savings_future_value(
        new_monthly, data['expected_return'], years_to_retirement
    )
    
    difference = new_future - current_future
    
    st.success(f"""
    💡 **Impact of saving ${extra_amount} more per month:**
    
    • Current plan: ${data['monthly_savings']}/month → ${current_future:,.0f} at retirement
    • New plan: ${new_monthly}/month → ${new_future:,.0f} at retirement
    • **Extra retirement income: ${difference:,.0f}**
    • That's ${difference/25/12:,.0f} more per month in retirement!
    """)

def show_what_if_retirement_age(years_change):
    data = st.session_state.user_data
    new_retirement_age = data['retirement_age'] + years_change
    new_years_to_retirement = new_retirement_age - data['age']
    
    if new_years_to_retirement <= 0:
        st.error("Invalid retirement age!")
        return
    
    # Calculate new totals
    current_savings_future = future_value(
        data['current_savings'], data['expected_return'], new_years_to_retirement
    )
    monthly_savings_future = monthly_savings_future_value(
        data['monthly_savings'], data['expected_return'], new_years_to_retirement
    )
    new_total = current_savings_future + monthly_savings_future
    
    # Original plan
    original_years = data['retirement_age'] - data['age']
    original_total = (future_value(data['current_savings'], data['expected_return'], original_years) + 
                     monthly_savings_future_value(data['monthly_savings'], data['expected_return'], original_years))
    
    difference = new_total - original_total
    
    action = "later" if years_change > 0 else "earlier"
    st.info(f"""
    ⏰ **Impact of retiring {abs(years_change)} years {action}:**
    
    • Original plan (age {data['retirement_age']}): ${original_total:,.0f}
    • New plan (age {new_retirement_age}): ${new_total:,.0f}
    • **Difference: ${difference:,.0f}**
    """)

def show_withdrawal_analysis(amount, monthly_withdrawal):
    data = st.session_state.user_data
    years_will_last = withdrawal_duration(amount, monthly_withdrawal, data['expected_return'])
    
    if years_will_last == float('inf'):
        st.success(f"""
        🎉 **Great news!** 
        
        ${amount:,} can support ${monthly_withdrawal:,}/month withdrawals **FOREVER** 
        at {data['expected_return']*100:.0f}% return rate!
        
        The interest income (${amount * data['expected_return'] / 12:,.0f}/month) 
        is higher than your withdrawals.
        """)
    else:
        st.warning(f"""
        ⏰ **Withdrawal Analysis:**
        
        • Starting amount: ${amount:,}
        • Monthly withdrawal: ${monthly_withdrawal:,}
        • At {data['expected_return']*100:.0f}% return: **{years_will_last:.1f} years**
        
        Your money will last until age {data['retirement_age'] + years_will_last:.0f}
        """)

def show_what_if_return_rate(new_rate):
    data = st.session_state.user_data
    years_to_retirement = data['retirement_age'] - data['age']
    
    # Calculate with new rate
    current_savings_future = future_value(data['current_savings'], new_rate, years_to_retirement)
    monthly_savings_future = monthly_savings_future_value(data['monthly_savings'], new_rate, years_to_retirement)
    new_total = current_savings_future + monthly_savings_future
    
    # Original rate calculation
    original_total = (future_value(data['current_savings'], data['expected_return'], years_to_retirement) + 
                     monthly_savings_future_value(data['monthly_savings'], data['expected_return'], years_to_retirement))
    
    difference = new_total - original_total
    
    st.info(f"""
    📊 **Impact of {new_rate*100:.0f}% vs {data['expected_return']*100:.0f}% return:**
    
    • At {data['expected_return']*100:.0f}%: ${original_total:,.0f}
    • At {new_rate*100:.0f}%: ${new_total:,.0f}
    • **Difference: ${difference:,.0f}**
    
    💡 Every 1% difference in returns = ${(new_total-original_total)/(new_rate-data['expected_return'])/100:,.0f} difference!
    """)

def handle_natural_language_questions():
    st.subheader("💬 Ask Me Anything About Your Finances")
    
    # Show example questions from PDF
    st.markdown("**Example questions I can answer:**")
    examples = [
        "I'm 35, save $1000 a month, expect 6% return—what age can I retire?",
        "If I'm retired with $400,000 and withdraw $3,000 a month at 5%, how long will it last?",
        "How much must I save monthly to reach $1 million in 25 years?",
        "What if inflation is 4%?",
        "Is it smarter to pay down my 3% mortgage or invest at 7%?"
    ]
    
    for example in examples:
        if st.button(f"📝 {example}", key=f"example_{hash(example)}"):
            answer = st.session_state.agent.process_question(example, st.session_state.user_data)
            st.success(f"**Answer:** {answer}")
    
    st.markdown("---")
    
    # Natural language input
    user_question = st.text_input("💭 Type your own financial question:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Get Answer") and user_question:
            answer = st.session_state.agent.process_question(user_question, st.session_state.user_data)
            st.info(f"**Answer:** {answer}")
    
    with col2:
        if st.button("Show Your Work") and user_question:
            answer = st.session_state.agent.process_question(user_question, st.session_state.user_data, show_work=True)
            st.markdown(f"**Detailed Answer:** {answer}")

# Main app logic
if st.session_state.step == 'input':
    collect_user_info()

elif st.session_state.step == 'analysis':
    show_analysis()
    
    st.markdown("---")
    handle_natural_language_questions()  # NEW: Natural language Q&A
    
    st.markdown("---") 
    handle_questions()  # KEEP: Your existing what-if scenarios
    
    # Reset button
    if st.button("🔄 Start Over"):
        st.session_state.clear()
        st.rerun()
# Sidebar
with st.sidebar:
    st.markdown("### 🧮 Quick Calculator")
    
    if st.session_state.user_data:
        data = st.session_state.user_data
        st.write(f"**{data['name']}'s Profile:**")
        st.write(f"• Age: {data['age']}")
        st.write(f"• Retirement: {data['retirement_age']}")
        st.write(f"• Savings: ${data['monthly_savings']}/month")
        st.write(f"• Return: {data['expected_return']*100:.0f}%")
    
    st.markdown("---")
    st.markdown("### 🔢 Mini Calculators")
    
    # Rule of 72
    rate_72 = st.number_input("Interest rate for Rule of 72", min_value=1, max_value=20, value=7)
    years_double = rule_of_72(rate_72)
    st.write(f"💰 Money doubles in **{years_double:.1f} years**")
    
    # Future Value
    pv = st.number_input("Present Value ($)", min_value=0, value=1000)
    fv_rate = st.number_input("Annual Rate (%)", min_value=0.0, max_value=20.0, value=7.0)
    fv_years = st.number_input("Years", min_value=1, max_value=50, value=10)
    fv_result = future_value(pv, fv_rate/100, fv_years)
    st.write(f"📈 Future Value: **${fv_result:,.0f}**")

    