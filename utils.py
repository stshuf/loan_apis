import numpy as np

def create_new_user_id(user_set):
	## Get highest id value, add another. Hypothetically this is a PK that the ORM will generate. 
	highest_user_id = max([int(i['id']) for i in user_set.values()])
	num = highest_user_id + 1
	return num

def generate_amortization_schedule(amount, interest_rate, loan_term):
    i_rate = interest_rate / 100
    monthly_payment = calculate_monthly_payment(amount, interest_rate, loan_term)
    ## Set remaing balance to inital loan amount. 
    remaining_balance = amount
    amortization_schedule = []

    m_range = loan_term + 1

    ## Iterate over each month of the term, include final month. 
    for i in range(1, m_range):
        get_monthly_data = get_month_balances(remaining_balance, monthly_payment, i_rate)

        ## Redeclare variable to use on next iteration.
        remaining_balance = get_monthly_data["remaining_balance"]
        
        amortization_schedule.append({
            "month": i,
            "remaining_balance": f"${remaining_balance:.2f}",
            "monthly_payment": f"${monthly_payment:.2f}",
        })
    
    return amortization_schedule

def calculate_monthly_payment(amount, interest_rate, loan_term):
	i_rate = interest_rate / 100
	r = i_rate / 12
	n = loan_term
	monthly_payment = (amount * r) / (1 - (1 + r) ** -n)
    
	return monthly_payment

def get_current_balances(loan_data, month_number):
	interest_rate = loan_data["rate"] / 100
	monthly_payment = calculate_monthly_payment(loan_data["amount"], interest_rate, loan_data["length"])
	monthly_interest_rate = interest_rate / 12
 
	## Assumption here is that the payments are made at the end of the month and interest applied
	## at the start of the month.
	amount = loan_data["amount"]

	## Set principal to og payment amount.
	principal_balance = amount
	total_principal_paid = 0
	total_interest_paid = 0
    
    ## Calculate interest paid and principal paid for each month of the term length. 
	for i in range(1, month_number+1):
		data = get_month_balances(principal_balance, monthly_payment, interest_rate)
		total_principal_paid += data["principal_paid"]
		total_interest_paid += data["interest_paid"]
		principal_balance = data["remaining_balance"]

	return {"principal balance": principal_balance, "total principal paid": total_principal_paid, "total interest paid": total_interest_paid}


def get_month_balances(remaining_balance, monthly_payment, interest_rate): 
	## Get interest paid for the month.
    interest_paid = remaining_balance * (interest_rate / 12)
    ## Difference between montly and interest is total principal paid. 
    principal_paid = monthly_payment - interest_paid
    
    ## Update remaining balance.
    remaining_balance -= principal_paid

    data = {
    	"interest_paid": interest_paid,
    	"principal_paid": principal_paid, 
    	"remaining_balance": remaining_balance,
    }

    return data
