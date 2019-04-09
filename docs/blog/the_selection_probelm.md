# The selection problem 

### Intro
It has been evident from the beginning that this project needed a database. But as a person with little knowledge of databases, it was not straightforward as to which one to pick. There were many options explored, from cloud hosted options to self hosted options, and even ones hosted locally on the development machine. All these had benefits and drawbacks that needed to be weighed against each other. Even after these options were considered there would be the question of what kind of database would we want. Relational, Key Value store, object storage, the list goes on. This blog explores what I tried, what worked, what didn’t work and what I chose and why.


### Goals
One of the main goals of the project was to run the application in a production environment and gather evidence as to whether it could work at scale, with speed as a customer facing product. This immediately ruled out the use of a database locally on a laptop. This left two options remaining for how I was going to host the project. I could use a server and deploy the database myself, or I could go to a cloud hosting provider and just rent a managed one from their. The end goal was I chose to rent a database from Amazon Web Services (AWS), but let me tell you why.

### Cost
Renting a server costs money, unless you have student credits for a service or you are on that platforms free tier. As I have been trying out deployment services throughout my degree, there are many platforms where I have run out of student credits. AWS is not one. AWS also has a free tier option, even for databases. Sometimes because databases require storage this is not always an option to have free tier of may cost lots of credits. This means that in money terms AWS was the cheapest option. 

### Time
Now the option remained, did I want to rent an Elastic Computing 2 (EC2) virtual server and install the database on that or did I want to rent a managed database that was already setup and ready to go? The option to me was obvious as a time saving method. Choosing the database that was preconfigured and pre managed was far cheaper in terms of time and why I chose to go with one of their pre configured options. 

### Style
You may think that okay we have chosen to go with AWS, that I almost us their, just click the button and you have a database at your fingertips. You would be correct in some ways in that assumption, because you can do just that (almost), but the problem that remained for me was, which one? Amazon has on offer databases from Redshift (A data warehousing database), to Dynamo (Key Value Store), S3 (Object storage) to all the traditional databases (MySQL, PostgreSQL). It was a job to figure out what one was best, and although at the end this may seem trivial, as a junior in the software development world this took weeks to scrutiny and thought. 

#### Object Store
My first option was one of lazy thought. It was the S3. I thought that I would already have each data point as a data object and so hearing the term object storage would store every key point as an object. This turned out to work great, but with one big gotya. Every “object” is like a file to S3, because it is designed to take files for backups and large unorganised storage, it’s a whole hot mess when you have large amounts of data that you want to access hundreds of times a second and search through that data. It also kinda makes the assumption that you know what file that you are looking for. Something that in this project we can almost guarantee that we will not know what we are looking for when we go to try and find it. S3 was crossed off the list.

#### Key Value
The second item that we tried was the dynamo database. This also worked. We used the url of where the image had come from as the key and the data point as the value. But that meant that everytime we wanted to find out if a data point was a match then we would have to go through each of the data points one by one and check if it was a match. While this may work this a database of even up to 20 data points, this would not scale to hundreds of thousands of data points, the goal of the project. This means that dynamo was again not an ideal candidate. 

#### Relational Database
This left us scratching our heads. How could we make this project search the database with speed. I then remembered indexing and relational databases. If we hashed the data points with a similarity hash then we could have a feeling as to how similar data points are based on the hash, pull out only a few and then match them with the data points. This lead to lots of research into what type of relational database we wanted to deploy. We found the with Postgres we could load in the extra functions and use the built in levenshtein distance to do the matching in the query to add speed. Pulling back only the data that we want. Postgres is also open source and seeing how everything so far in this project is we can also stick with that theme. 

### Conclusion
So this was a short justification as to why I am using a relational database and how I changed the underlying design of the project to be able to speed up significantly the search for similar data points in the project. While this blog may not provide any new information I believe that it demonstrates the ability to always do better and redesign even if things work, by stepping back and asking if you are using the correct tool for the job, you can often see flaws in that you are working on.

