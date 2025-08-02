# 💰 AI Financial Planning Agent

> **Ask questions in plain English. Get instant, personalized financial advice. Completely free.**

![Financial Planning Agent](https://github.com/aryaanushka/Financial-Agent/blob/main/Screenshot.png)

*Replace `yourusername` with your actual GitHub username and upload your screenshot*

## 🎯 What This Does

Transform complex financial planning into simple conversations. Ask "*What age can I retire?*" and get instant, detailed answers with step-by-step math explanations.

## ⚡ Quick Demo

```
You: "I'm 30, save $800/month, expect 7% return—when can I retire?"
Agent: "Based on saving $800/month at 7% return, you can retire at age 58."

Click "Show Your Work" to see the exact formulas and calculations.
```

## 🚀 Features

| Feature | Description |
|---------|-------------|
| **🤖 Smart Q&A** | Ask financial questions in natural language |
| **📊 Show Your Work** | See step-by-step formula explanations |
| **⚡ Instant Analysis** | Complete retirement projection in seconds |
| **🎨 Visual Charts** | Interactive growth and scenario comparisons |
| **🔒 100% Private** | No data leaves your computer |

## 📋 Quick Start

**1. Clone & Install**
```bash
git clone https://https://github.com/aryaanushka/Financial-Agent.git
cd financial-planning-agent
pip install streamlit pandas plotly
```

**2. Run**
```bash
streamlit run app.py
```

**3. Open** → `http://localhost:8501`

That's it! No API keys, no registration, no complexity.

## 💬 Ask These Questions

- *"I'm 35, save $1000/month, expect 6% return—what age can I retire?"*
- *"How long will $500k last if I withdraw $3k monthly?"*
- *"How much must I save monthly to reach $1 million in 20 years?"*
- *"What if inflation is 4%?"*
- *"Should I pay my 3% mortgage or invest at 7%?"*

## 🧮 What It Calculates

✅ **Retirement Age** - When you can stop working  
✅ **Money Duration** - How long savings will last  
✅ **Savings Targets** - Monthly amount needed for goals  
✅ **Inflation Impact** - Future expense projections  
✅ **Investment vs Debt** - Which strategy wins  

## 📊 Example Results

**Question**: *"I'm 25, save $500/month, want to retire at 60 with $1M"*

**Answer**: 
```
You'll have $1,379,843 by age 60! 
✅ Goal exceeded by $379,843
📈 That's $4,599/month retirement income
```

**Show Your Work**:
```
Formula Used: Future Value of Annuity
• Monthly savings: $500
• Time period: 35 years  
• Expected return: 7%
• Total contributions: $210,000
• Growth from compound interest: $1,169,843
```

## 🎨 Visual Features

- **Growth Chart**: Watch your money grow year by year
- **Scenario Table**: Compare 5 different strategies instantly  
- **Impact Analysis**: See how small changes create big results

## 🔧 Built With

- **Python + Streamlit** (Web interface)
- **Financial Math** (Time value of money formulas)
- **Smart Parsing** (Understands natural language)
- **Zero Dependencies** (No external APIs)

## 📁 File Structure

```
📦 financial-agent
├── 🚀 app.py              # Main interface
├── 🤖 agent.py            # Question processing  
├── 📊 financial_formulas.py # Math engine
└── 📋 requirements.txt    # Dependencies
```

## 🎯 Perfect For

- **Students** learning financial planning
- **Young Professionals** starting retirement planning  
- **Career Changers** adjusting financial goals
- **Anyone** wanting to understand money growth

## 🧪 Test It

```bash
python test_agent.py
```
Runs 15+ test scenarios to verify accuracy.

## 💡 Why This Rocks

| Traditional Calculators | This Agent |
|------------------------|------------|
| Multiple separate tools | One intelligent interface |
| Complex forms to fill | Natural conversation |
| Results without explanation | Shows the math |
| Static analysis | Dynamic what-if scenarios |
| Intimidating for beginners | Friendly and educational |

## 🔒 Privacy

- ✅ **Runs locally** - Your data never leaves your computer
- ✅ **No tracking** - Anonymous usage  
- ✅ **No accounts** - Open and use immediately
