PRAGMA foreign_keys;
BEGIN TRANSACTION;

drop table if exists Users;
create table Users (
  username string primary key not null,
  email string not null,
  pass password not null
);

drop table if exists Followers;
create table Followers (
  username string,
  usernamefollowing string,
  foreign key (username) references Users (username),
  foreign key (usernamefollowing) references Users (username)
);

drop table if exists Tweets;
create table Tweets (
  username string not null,
  tweet string not null,
  time_stamp timestamp DEFAULT (DATETIME('now', 'localtime'))
);

insert into Users (username, email, pass) values ('ankita', 'ankita@gmail.com', '0b923db03c8718ad3b5d3a885442ff03');
insert into Users (username, email, pass) values('aditi', 'aditi@gmail.com', 'b589dfbf1c1c742de1ef73e77324310b');
insert into Users (username, email, pass) values('shraddha', 'shraddha@gmail.com', '174037c99c15ad0ec6f6ff755eb0e3a8');
insert into Users (username, email, pass) values('brian', 'Brian@gmail.com', '51f1599a923b58ca176e0ac5bf34ae8c');
insert into Users (username, email, pass) values('mark', 'Mark@gmail.com', 'd1af90699f2a2c983e6ccb7bee874414');

insert into Followers (username, usernamefollowing) values ('ankita', 'aditi');
insert into Followers (username, usernamefollowing) values ('aditi', 'shraddha');
insert into Followers (username, usernamefollowing) values ('shraddha', 'ankita');
insert into Followers (username, usernamefollowing) values ('ankita', 'shraddha');

insert into Tweets (username, tweet) values ('ankita', 'My First Tweet');
insert into Tweets (username, tweet) values ('aditi', 'Hurray');
insert into Tweets (username, tweet) values ('ankita', 'Hey you all!!');

COMMIT;