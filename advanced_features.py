import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from financial_formulas import *

def create_growth_chart(user_data):
    """Create a chart showing money growth over time"""
    years_to_retirement = user_data['retirement_age'] - user_data['age']
    
    # Create year-by-year data
    years = list(range(years_to_retirement + 1))
    current_savings_growth = []
    monthly_savings_growth = []
    total_growth = []
    
    for year in years:
        # Current savings growth
        current_val = future_value(user_data['current_savings'], user_data['expected_return'], year)
        current_savings_growth.append(current_val)
        
        # Monthly savings accumulation
        if year == 0:
            monthly_val = 0
        else:
            monthly_val = monthly_savings_future_value(
                user_data['monthly_savings'], user_data['expected_return'], year
            )
        monthly_savings_growth.append(monthly_val)
        
        total_growth.append(current_val + monthly_val)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Year': years,
        'Age': [user_data['age'] + y for y in years],
        'Current Savings Growth': current_savings_growth,
        'Monthly Savings Growth': monthly_savings_growth,
        'Total': total_growth
    })
    
    # Create stacked area chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Age'], y=df['Current Savings Growth'],
        fill='tonexty', mode='lines',
        name=f'Current ${user_data["current_savings"]:,} Growing',
        line=dict(color='lightblue')
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Age'], y=df['Total'],
        fill='tonexty', mode='lines',
        name=f'Monthly ${user_data["monthly_savings"]:,} Added',
        line=dict(color='darkblue')
    ))
    
    fig.update_layout(
        title=f"Your Money Growth to Age {user_data['retirement_age']}",
        xaxis_title="Age",
        yaxis_title="Account Value ($)",
        yaxis_tickformat='$,.0f',
        hovermode='x unified'
    )
    
    return fig

def retirement_scenarios_table(user_data):
    """Create table showing different scenarios"""
    base_years = user_data['retirement_age'] - user_data['age']
    
    scenarios = [
        {"Scenario": "Current Plan", "Monthly": user_data['monthly_savings'], "Years": base_years, "Return": user_data['expected_return']},
        {"Scenario": "Save $200 More", "Monthly": user_data['monthly_savings'] + 200, "Years": base_years, "Return": user_data['expected_return']},
        {"Scenario": "Retire 2 Years Later", "Monthly": user_data['monthly_savings'], "Years": base_years + 2, "Return": user_data['expected_return']},
        {"Scenario": "Conservative (5%)", "Monthly": user_data['monthly_savings'], "Years": base_years, "Return": 0.05},
        {"Scenario": "Aggressive (9%)", "Monthly": user_data['monthly_savings'], "Years": base_years, "Return": 0.09},
    ]
    
    results = []
    for scenario in scenarios:
        current_future = future_value(user_data['current_savings'], scenario['Return'], scenario['Years'])
        monthly_future = monthly_savings_future_value(scenario['Monthly'], scenario['Return'], scenario['Years'])
        total = current_future + monthly_future
        monthly_income = total / 25 / 12  # Assume 25 years retirement
        
        results.append({
            "Scenario": scenario['Scenario'],
            "Monthly Savings": f"${scenario['Monthly']:,}",
            "Years Saving": scenario['Years'],
            "Total at Retirement": f"${total:,.0f}",
            "Monthly Income": f"${monthly_income:,.0f}"
        })
    
    return pd.DataFrame(results)