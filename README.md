# loan_apis

Two datasets have already been created, one containing unique user data and the other containing unique loan data. 


To get started: 
- Install unvicorn 
- Intall pydantic 

Once installed, navigate to folder, and run command: 
source bin/activate 

Navigate to local enviorment, usually: http://127.0.0.1:8000/ 

The easiest way to work through and manipulate the apis is accessing: http://127.0.0.1:8000/docs 
This will allow you to see all endpoints that are avaiable along with the parameters that are expected. 




A few notes: 
- Ideally, these apis would not be working off json files, but actual database information 
- For monthly payments and interest, I assumed payments are made at the end of the month 
	and interest applied at the start of the month.
- The root will show all user data,  