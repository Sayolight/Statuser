# Sayo.Statuser
Set your status to telegram user avatar

# How to use

* Install *telethon* and *dotenv* modules
* Enter to .env file your *api_id* and *hash_id* ([Find it here](https://my.telegram.org/))
* Login to Telegram in **main.py**
* Get JsonStorage token in **main.py** and write it to .env file
* To change status - write to Saved Messages: "$statuser *avatar*" or use PUT Request to JsonStorage

# PUT Requests
Data: {'status': '*statusname*'}

Example: 
```
$.ajax({
    url:"https://jsonstorage.net/api/items/{id}",
    type:"PUT",
    data:'{"status":"statusname"}',
    contentType:"application/json; charset=utf-8",
    dataType:"json",
    success: function(data, textStatus, jqXHR){
    
    }
});
```
https://jsonstorage.net/
