from datetime import datetime
curr_dt = datetime.now()
 
print("Current datetime: ", curr_dt)
timestamp = int(round(curr_dt.timestamp()))
 
print("Integer timestamp of current datetime: ",
      timestamp)