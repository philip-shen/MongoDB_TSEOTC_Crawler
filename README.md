MongoDB_TSEOTC_Crawler
==============================
TW TSE&amp;OTC OHLC Price Crawler to store in MongoDB


Sequence Diagram
==============================
![alt tag](https://i.imgur.com/0HBUWEK.jpg)
(Diagram made with [js-sequence-diagrams](https://bramp.github.io/js-sequence-diagrams/))


MongoDB Bulk Insertion Test:
==============================
* Step 1
Edit file config.ini to meet your setting
``` 
[MONGODB]
;modify below those variables to meet your configuration
mongo_host = mongo_ip
mongo_db = TWStockDB
mongo_collection = TSEOTC
mongo_username = username
mongo_password = password

[SeymourExcel]
last_year_month=2018,10
stkidx = 2892
delay_sec = 1
``` 

* Step 2
![alt tag](https://i.imgur.com/emeTmtP.jpg)

* Step 3
Testing to connect MongoDB via Robo 3T

![alt tag](https://i.imgur.com/Gu00xWM.jpg)

Check DB and browse document and collections

![alt tag](https://i.imgur.com/m2VXbHx.jpg)


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
o pymongo 3.7.2。
``` 

Reference 
==============================
* [Setting up and connecting to a remote MongoDB database](https://medium.com/founding-ithaka/setting-up-and-connecting-to-a-remote-mongodb-database-5df754a4da89)
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

* [Tutorial Bulk Inserts](http://api.mongodb.com/python/current/tutorial.html#bulk-inserts)
* [MongoDB pymongo bulk update all documents in a collection](https://gist.github.com/messa/4407772e87c61e193b3bf2a777a6e0e0)

* [MongoDB Schema 設計指南](http://blog.toright.com/posts/4537/mongodb-schema-%E8%A8%AD%E8%A8%88%E6%8C%87%E5%8D%97-part-ii-%E5%8F%8D%E6%AD%A3%E8%A6%8F%E5%8C%96%E7%9A%84%E5%A8%81%E5%8A%9B.html)
* [MongoDB Schema 設計指南 (Part II) – 反正規化的威力](http://blog.toright.com/posts/4537/mongodb-schema-%E8%A8%AD%E8%A8%88%E6%8C%87%E5%8D%97-part-ii-%E5%8F%8D%E6%AD%A3%E8%A6%8F%E5%8C%96%E7%9A%84%E5%A8%81%E5%8A%9B.html)
* [MongoDB 教學 – 如何備份與還原 MongoDB](http://blog.toright.com/posts/4069/mongodb-%E6%95%99%E5%AD%B8-%E5%A6%82%E4%BD%95%E5%82%99%E4%BB%BD%E8%88%87%E9%82%84%E5%8E%9F-mongodb.html)
* [MongoDB Replica Set 高可用性架構搭建](http://blog.toright.com/posts/4508/mongodb-replica-set-%E9%AB%98%E5%8F%AF%E7%94%A8%E6%80%A7%E6%9E%B6%E6%A7%8B%E6%90%AD%E5%BB%BA.html)
* [MongoDB Sharding 分散式儲存架構建置 (概念篇)](http://blog.toright.com/posts/4552/mongodb-sharding-%E5%88%86%E6%95%A3%E5%BC%8F%E5%84%B2%E5%AD%98%E6%9E%B6%E6%A7%8B%E5%BB%BA%E7%BD%AE-%E6%A6%82%E5%BF%B5%E7%AF%87.html)
* [MongoDB Sharding 分散式儲存架構建置 (實作篇)](http://blog.toright.com/posts/4574/mongodb-sharding-%E5%88%86%E6%95%A3%E5%BC%8F%E5%84%B2%E5%AD%98%E6%9E%B6%E6%A7%8B%E5%BB%BA%E7%BD%AE-%E5%AF%A6%E4%BD%9C%E7%AF%87.html)

* [Replication](https://docs.mongodb.com/v3.6/replication/)

* [jang0820/Stock/FromTwseToMongo.py](https://github.com/jang0820/Stock/blob/master/FromTwseToMongo.py)

* []()
![alt tag]()