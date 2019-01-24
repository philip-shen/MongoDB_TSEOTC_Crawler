MongoDB_TSEOTC_Crawler
==============================
TW TSE&amp;OTC OHLC Price Crawler to store in MongoDB

MongoDB Setup:
==============================
* Step 1
MongoDB command shell
``` 
$ mongo
``` 
![alt tag](https://i.imgur.com/hCcWrqZ.jpg)

* Step 2
Disable MongoDB Auth
``` 
$ sudo vim /etc/mongod.conf
``` 

In this file remark the following lines:
``` 
#security:
#    authorization: 'enabled'
``` 

Now save and exit the config file and restart mongodb server.
``` 
$ sudo service mongod restart
``` 

* Step 3
Swtich to Admin and Create Read/Write Privilege for User
``` 
> ~$ mongo --port 27017 -u "admin" -p "adminpassword" --authenticationDatabase "admin"
``` 

``` 
> db.grantRolesToUser( "philshen", [ "dbAdmin" , { role: "dbAdmin", db: "TWStockDB" } ] );

> db.grantRolesToUser( "philshen", [ "readWrite" , { role: "readWrite", db: "TWStockDB" } ] );
``` 

![alt tag](https://i.imgur.com/XU4VQ8n.jpg)


* Step 4
Enable MongoDB Auth

``` 
$ sudo vim /etc/mongod.conf
``` 

In this file add the following lines:
``` 
security:
    authorization: 'enabled'
``` 

Now save and exit the config file and restart mongodb server.
``` 
$ sudo service mongod restart
``` 

* Step 5
Testing to connect MongoDB via Robo 3T

![alt tag](https://i.imgur.com/r7aYl0x.jpg)

TroubleShooting
==============================
* [MongoDB: db.grantRolesToUser() method](https://www.w3resource.com/mongodb/shell-methods/user-management/db-grantRolesToUser.php)

``` 
use admin
db.grantRolesToUser(
   "mynewuser",
   [ "readWrite" , { role: "read", db: "orders" } ],
   { w: "majority" , wtimeout: 4000 }
);
``` 

* [MongoDB: db.updateUser() method](https://www.w3resource.com/mongodb/shell-methods/user-management/db-updateUser.php)
``` 
db.updateUser( "mynewuser",
               {
                 customData : { employeeId : "0x3039" },
                 roles : [
                           { role : "read", db : "assets"  }
                         ]
                }
             );
``` 

* [MongoDB: db.dropUser() method](https://www.w3resource.com/mongodb/shell-methods/user-management/db-dropUser.php)
``` 
> db.dropUser("mynewuser", {w: "majority", wtimeout: 4000});
true
``` 


Environment
==============================
``` 
o Ubuntu 16.04.5 LTS (GNU/Linux 4.15.0-1026-gcp x86_64)。
o MongoDB 3.6。
o Robo 3T 1.2.1。
o Python 3.6。
``` 

Reference 
==============================
* [[mongodb]增加mongoDB效能的技巧](https://blog.xuite.net/flyingidea/blog/67641474)
* [[mongoDB]index功能的筆記](https://blog.xuite.net/flyingidea/blog/68050501)
* [[Python] Pandas dataframe 資料儲存至 MongoDB](https://oranwind.org/python-pandas-ji-chu-jiao-xue-2/)
* [Flask扩展系列(五)–MongoDB](http://www.bjhee.com/flask-ext5.html)
* [Python利用ORM控制MongoDB（MongoEngine）的步骤全纪录](https://www.jb51.net/article/147379.htm)
* [Python與資料分析](https://sites.google.com/site/zsgititit/shi-yongpython-jin-xing-zi-liao-fen-xi)
* [connecting to MongoDB with authentication using pymongo 2.7](https://stackoverflow.com/questions/41769875/connecting-to-mongodb-with-authentication-using-pymongo-2-7)
``` 
After created a db and put some docs into collection, should also createUser() for that db, than pymongo can access.
``` 

* [Centralized User Data](https://docs.mongodb.com/v3.6/core/security-users/#centralized-user-data)
``` 
Changed in version 2.6.

MongoDB stores all user information, including name, password, and the user's authentication database, in the system.users collection in the admin database.

Do not access this collection directly but instead use the user management commands.
``` 

* [MongoDB: db.updateUser() method](https://www.w3resource.com/mongodb/shell-methods/user-management/db-updateUser.php)
* [MongoDB: db.dropUser() method](https://www.w3resource.com/mongodb/shell-methods/user-management/db-dropUser.php)
* [MongoDB: db.grantRolesToUser() method](https://www.w3resource.com/mongodb/shell-methods/user-management/db-grantRolesToUser.php)

* [MongoError: not authorized on to execute command { find: “app_updates”, filter: { key: “0.0.1-admins” }, limit: 1, batchSize: 1, singleBatch: true }](https://stackoverflow.com/questions/47130379/mongoerror-not-authorized-on-to-execute-command-find-app-updates-filter)
* [Mongodb enable authentication (Enable Access Control)](https://medium.com/@raj_adroit/mongodb-enable-authentication-enable-access-control-e8a75a26d332)

* []()
![alt tag]()