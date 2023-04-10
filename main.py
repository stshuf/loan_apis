from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import date
import array
import utils 
import json

## Kick start fast api. 
app = FastAPI()

## Set BaseModels for each obj. 
class userObj(BaseModel):
	u_id: Optional[int] = None
	name: str
	age: int 
	martial_status: str 
	sharing_info_with : Optional[int] = None

class loanObj(BaseModel):
	l_id: Optional[int] = None 
	created: Optional[str] = None 
	modifed: Optional[str] = None
	length: int 
	is_paid_off: int
	amount: int 
	rate: float 
	monthly_amount: int 
	user_id: int 


## Cache all current files. This will live in a DB so we wont need to do this in real life.
user_file = open("user_set.json")
all_users = json.load(user_file)
user_file.close()

loan_file = open("loan_set.json")
all_loans = json.load(loan_file)
loan_file.close()

@app.get("/")
def show_all_data():
	return all_users, all_loans

@app.get("/get_user")
def get_user(user_id: int = Query(None, title="User_id", description="User id as it appears in dataset.")):
	msg = "ok"
	get_user = [user_obj for key, user_obj in all_users.items() if user_obj["id"] == user_id]

	if len(get_user) > 0:
		user = get_user[0]
	else:
		msg = "## User ID {user_id} does not exist."	
		user = None
	return msg, user

@app.post("/create_user/")
def create_user(user: userObj, status_code=201):
	## Need to set up a unique id so take the max amount we have now add one. 
	## Ideally the DB will do this, but since we are are working with a data set. Do it for us.
	user_id = utils.create_new_user_id(all_users)
	try: 
		new_user = {
			"id": user_id,
			"name": user.name,
			"age": user.age,
			"martial_status": user.martial_status,
			"sharing_info_with": user.sharing_info_with
		}
		all_users[user_id] = new_user
	except Exception as e: 
		return HTTPException(status_code=400, detail=f"Invalid data provided for new user {user}")

	return new_user

@app.post("/create_loan/",status_code=201)
def create_loan(loan: loanObj):
	loan_id = utils.create_new_user_id(all_loans)
	today = date.today()
	timestamp = today.strftime("%Y-%m-%d")
	try: 
		new_loan = {
			"id": loan_id,
			"created": timestamp,
			"modifed": timestamp, 
			"length": loan.length, 
			"is_paid_off": 0, 
			"amount": loan.amount,
			"rate": loan.rate,
			"monthly_amount": loan.monthly_amount,
			"user_id": loan.user_id
		}

		all_loans[loan_id] = new_loan
	except Exception as e: 
		return HTTPException(status_code=400, detail=f"Invalid loan data provided for new loan agreement {user}")

	return new_loan

@app.get("/get_schedule/{loan_id}", status_code=200)
def get_loan_schedule(loan_id: int):
	get_loan = [l for l in all_loans.values() if l['id'] == loan_id]
	loan_data = get_loan[0]
	schedule = utils.generate_amortization_schedule(loan_data["amount"], loan_data["rate"], loan_data["length"])
	
	return msg, schedule

@app.get("/get_summary/", status_code=200)
def get_monthly_summary(loan_id: int, month_number: int):
	msg = 'ok'
	get_loan = [l for l in all_loans.values() if l['id'] == loan_id]
	loan_data = get_loan[0]
	
	amortization_schedule = utils.generate_amortization_schedule(loan_data["amount"], loan_data["rate"], loan_data["length"])
	get_amounts = utils.get_current_balances(loan_data, month_number)

	return msg, get_amounts 

@app.get("/get_loans", status_code=200)
def get_loans(user_id: Optional[int] = Query(None, title="User_id", description="User id as it appears in dataset."), 
				name: Optional[str] = Query(None, title="Name", description="User Name")):
	msg = 'ok'
	user = ['']

	if user_id is None and name is None: 
		return HTTPException(status_code=404, detail=f"Please specify a user you'd like to search.")

	elif user_id is not None and name is not None: 
		## Chose to do a partial match instead of an exact match. 
		## People have trouble spelling so wanted to give them some slack. Also if there are families.
		user = [u for u in all_users.values() if u["id"] == user_id and name.lower() in u["name"].lower()]
	else: 
		if user_id is None: 
			user = [u for u in all_users.values() if name.lower() in u["name"].lower()]
		else:
			user = [u for u in all_users.values() if u["id"] == user_id]

	if len(user) > 1:
		msg = "Multiple Users found with those parameters"
	elif not user:
		return HTTPException(status_code=404, detail=f"No users found with those parameters.")

	return msg, user

@app.put("/share_loan", status_code=204)
def share_loan(user_id: int, account_to_be_added: int):
	msg = 'ok'
	main_user_account = [u for u in all_users.values() if u["id"] == user_id][0]
	account_to_be_shared = [u for u in all_users.values() if u["id"] == account_to_be_added][0]

	if not main_user_account or not account_to_be_added: 
		return HTTPException(status_code=404, detail=f"No users found with those parameters: {user_id}")

	main_user_account['sharing_info_with'].append(account_to_be_shared["id"])

	return main_user_account


