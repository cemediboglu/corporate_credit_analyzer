# Corporate Credit Analyzer v0.1
# Global bank-grade internal rating model simulation
# Author: Cem Ediboglu – Credit Analyst
print("=" * 70)
print("    GLOBAL BANK – CORPORATE CREDIT RATING ENGINE    ".center(70))
print("=" * 70)
print("This tool calculates internal credit rating and")
print("recommended maximum facility limit for corporate clients.\n")

print("Step 1 completed – Corporate credit analysis engine started!")
print("=" * 70)

# --- INPUT SECTION ---
print("Please enter the following financial figures (in million USD):")
print("-" * 60)
company_name = input("Company name                : ").strip()

# Financial inputs
revenue      = float(input("Annual Revenue (turnover)   : "))
ebitda       = float(input("EBITDA                      : "))
total_debt   = float(input("Total Debt                  : "))
interest_exp = float(input("Annual Interest Expense     : "))
current_assets = float(input("Current Assets            : "))
current_liabilities = float(input("Current Liabilities      : "))

print("\nData successfully loaded for:", company_name)
print("=" * 70)

# --- CALCULATION SECTION ---
print("Calculating key financial ratios...")
print("-" * 50)

# Safe division to avoid division by zero
def safe_div(numerator, denominator, default=999.0):
    return numerator / denominator if denominator != 0 else default

leverage_ratio       = safe_div(total_debt, ebitda)                          # Total Debt / EBITDA
interest_coverage    = safe_div(ebitda, interest_exp)                       # EBITDA / Interest Expense
ebitda_margin        = safe_div(ebitda, revenue) * 100                     # EBITDA Margin (%)
current_ratio        = safe_div(current_assets, current_liabilities)       # Current Ratio

print(f"Leverage Ratio (Total Debt / EBITDA)      : {leverage_ratio:.2f}x")
print(f"Interest Coverage (EBITDA / Interest)     : {interest_coverage:.2f}x")
print(f"EBITDA Margin                             : {ebitda_margin:.1f}%")
print(f"Current Ratio                             : {current_ratio:.2f}x")
print("=" * 70)

# --- RATING SECTION ---
print("Applying internal rating scorecard...")
print("-" * 50)

# Score calculation for each factor (1 = worst, 5 = best)

def score_leverage(ratio):
    if ratio <= 1.5:   return 5
    elif ratio <= 2.5: return 4
    elif ratio <= 4.0: return 3
    elif ratio <= 6.0: return 2
    else: return 1

def score_coverage(ratio):
    if ratio >= 8.0:   return 5
    elif ratio >= 5.0: return 4
    elif ratio >= 3.0: return 3
    elif ratio >= 1.5: return 2
    else:              return 1

def score_margin(percent):
    if percent >= 30:  return 5
    elif percent >= 20: return 4
    elif percent >= 12: return 3
    elif percent >= 5:  return 2
    else:              return 1

def score_liquidity(ratio):
    if ratio >= 2.0:   return 5
    elif ratio >= 1.5: return 4
    elif ratio >= 1.2: return 3
    elif ratio >= 1.0: return 2
    else:              return 1

def score_size(revenue_musd):
    if revenue_musd >= 10000: return 5
    elif revenue_musd >= 5000:  return 4
    elif revenue_musd >= 2000:  return 3
    elif revenue_musd >= 500:   return 2
    else:                       return 1

# Calculate individual scores
s1 = score_leverage(leverage_ratio)
s2 = score_coverage(interest_coverage)
s3 = score_margin(ebitda_margin)
s4 = score_liquidity(current_ratio)
s5 = score_size(revenue)

# Weighted average score
total_score = (s1*30 + s2*25 + s3*20 + s4*15 + s5*10) / 100

# Convert to internal rating (AAA to D)
rating_scale = {
    (4.5, 5.0): "AAA", (4.0, 4.5): "AA",  (3.5, 4.0): "A",
    (3.0, 3.5): "BBB",(2.5, 3.0): "BB", (2.0, 2.5): "B",
    (1.0, 2.0): "CCC", (0.0, 1.0): "D"
}

internal_rating = "D"
for (low, high), grade in rating_scale.items():
    if low <= total_score < high:
        internal_rating = grade
        break

print(f"Internal Credit Rating : {internal_rating} ({total_score:.2f}/5.00)")
print("=" * 70)

# --- OUTPUT SECTION ---
print("CREDIT DECISION REPORT".center(70))
print("=" * 70)

# Suggested maximum facility (simple but realistic rule)
# Rule: Max facility = EBITDA × multiplier according to rating

multipliers = {
    "AAA": 6.0, "AA": 5.5, "A": 5.0,
    "BBB": 4.0, "BB": 3.5, "B": 2.8,
    "CCC": 1.5, "D": 0.0
}

multiplier = multipliers.get(internal_rating, 0.0)
max_facility_musd = ebitda * multiplier

# Recommended spread over base rate (bps)
spread_bps = {
    "AAA": 80,  "AA": 100, "A": 130,
    "BBB": 180, "BB": 280, "B": 450,
    "CCC": 800, "D": 9999
}

recommended_spread = spread_bps.get(internal_rating, 9999)

print(f"Company                : {company_name.upper()}")
print(f"Annual Revenue         : ${revenue:,.0f}M")
print(f"EBITDA                 : ${ebitda:,.0f}M")
print(f"Total Debt             : ${total_debt:,.0f}M")
print(f"Internal Rating        : {internal_rating} ({total_score:.2f}/5.00)")
print("-" * 70)
print(f"Maximum Facility Limit : ${max_facility_musd:,.0f}M")

if multiplier > 0:
    print(f"Recommended Spread     : +{recommended_spread} bps")
else:
    print("Recommended Spread     : DECLINED")
print("=" * 70)

if internal_rating in ["AAA", "AA", "A", "BBB"]:
    decision = "APPROVED"
elif internal_rating in ["BB", "B"]:
    decision = "APPROVED WITH CAUTION"
else:
    decision = "DECLINED"

print(f"FINAL DECISION         : {decision}".center(70))
print("=" * 70)





