import numpy as np

def create_new_user_id(user_set):
	## Get highest id value, add another. Hypothetically this is a PK that the ORM will generate. 
	highest_user_id = max([int(i['id']) for i in user_set.values()])
	num = highest_user_id + 1
	return num

def generate_amortization_schedule(amount, interest_rate, loan_term, month_range=None):
    i_rate = interest_rate / 100
    monthly_payment = calculate_monthly_payment(amount, interest_rate, loan_term)
    ## Set remaing balance to inital loan amount. 
    remaining_balance = amount
    amortization_schedule = []

    if month_range is None: 
    	month_range = loan_term + 1
    else: 
    	## Make it inclusive.
    	month_range = month_range + 1

    ## Iterate over each month of the term, include final month. 
    for i in range(1, month_range):
    	## Get interest paid for the month.
        interest_paid = remaining_balance * (i_rate / 12)
        ## Diffrence between montly and interest is total prinipal paid. 
        principal_paid = monthly_payment - interest_paid
        
        ## Update remaining balance.
        remaining_balance -= principal_paid
        
        amortization_schedule.append({
            "month": i,
            "remaining_balance": f"${remaining_balance:.2f}",
            "monthly_payment": f"${monthly_payment:.2f}",
            "principal_paid": principal_paid,
            "interest_paid": interest_paid,
        })
    
    return amortization_schedule

def calculate_monthly_payment(amount, interest_rate, loan_term):
	i_rate = interest_rate / 100
	r = i_rate / 12
	n = loan_term
	monthly_payment = (amount * r) / (1 - (1 + r) ** -n)
    
	return monthly_payment

def get_current_balances(loan_data, month_number):

	var = generate_amortization_schedule(loan_data["amount"], loan_data["rate"], loan_data["length"], month_number)


	# ## Assumption here is that the payments are made at the end of the month and interest applied
	# ## at the start of the month.
	# amount = loan_data["amount"]
	# annual_interest_rate = loan_data["rate"] / 100
	# loan_term_months = loan_data["length"]

	# ## Calculate monthly interest and payment.
	# monthly_interest_rate = annual_interest_rate / 12
	# monthly_payment = (amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -loan_term_months)
	
	# ## Set principal to og payment amount.
	# principal_balance = amount
	# total_principal_paid = 0
	# total_interest_paid = 0
	# print(float(monthly_payment))
    
    # ## Calculate interest paid and principal paid for each month of the term length. 
	# for i in range(1, month_number + 1):
	# 	interest_paid = principal_balance * monthly_interest_rate
	# 	total_interest_paid += interest_paid
	# 	principal_paid = monthly_payment - interest_paid
	# 	total_principal_paid += principal_paid
	# 	principal_balance -= principal_paid
    
	return var #{"principal balance": principal_balance, "total principal paid": total_principal_paid, "total interest paid": total_interest_paid}




