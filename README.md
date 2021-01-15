# Sayo.Statuser
Set your status to telegram user avatar

# How to use

* Install *telethon*, *PIL*, *requests* and *dotenv* modules
* Enter to .env file your *api_id* and *hash_id* ([Find it here](https://my.telegram.org/))
* Login to Telegram in **main.py**
* Get jsonbox.io token in **main.py** and write it to .env file
* Create telegram channel for statuser and enter if of this channel to .env file
* To update your avatar without status - pin to created channel your image 
* To change status - write to created channel: "s *avatar*" or use PUT Request to jsonbox.io

# PUT Requests
Data: {'status': '*statusname*'}

Example: 
```
$.ajax({
    url:"https://jsonbox.io/************************/***********************",
    type:"PUT",
    data:'{"status":"statusname"}',
    contentType:"application/json; charset=utf-8",
    dataType:"json",
    success: function(data, textStatus, jqXHR){
    
    }
});
```
https://jsonbox.io/
