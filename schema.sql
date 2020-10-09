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

insert into Users (username, email, pass) values ('ankita', 'ankita@gmail.com', 'ankita@123');
insert into Users (username, email, pass) values('aditi', 'aditi@gmail.com', 'aditi@123');
insert into Users (username, email, pass) values('shraddha', 'shraddha@gmail.com', 'shraddha@123');
insert into Users (username, email, pass) values('brian', 'Brian@gmail.com', 'Brian@123');
insert into Users (username, email, pass) values('mark', 'Mark@gmail.com', 'Mark@123');

insert into Followers (username, usernamefollowing) values ('ankita', 'aditi');
insert into Followers (username, usernamefollowing) values ('aditi', 'shraddha');
insert into Followers (username, usernamefollowing) values ('shraddha', 'ankita');
insert into Followers (username, usernamefollowing) values ('ankita', 'shraddha');

insert into Tweets (username, tweet) values ('ankita', 'My First Tweet');
insert into Tweets (username, tweet) values ('aditi', 'Hurray');
insert into Tweets (username, tweet) values ('ankita', 'Hey you all!!');

COMMIT;