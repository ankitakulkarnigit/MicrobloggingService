# MicrobloggingService

Steps to run:

Terminal 1:

$ export FLASK_APP=UsersMicroservice.py
$ flask init
$ python3 UsersMicroservice.py

Terminal 2:
On a second terminal execute all the curl commands from the commented section of UsersMicroservice.py for eg:

$ curl -i -X POST -H 'Content-Type:application/json' -d '{"usernameAPI":"newuser", "emailAPI":"newuser@gmail.com", "passwordAPI":"newuser@1234"}' http://localhost:5000/createUser;
$ curl -i -X GET -H 'Content-Type:application/json' -d '{"usernameAPI":"om", "passwordAPI":"om@123"}' http://localhost:5000/authenticateUser;
$ curl -i -X POST -H 'Content-Type:application/json' -d '{"usernameAPI":"om", "usernameFollowingAPI":"ankita"}' http://localhost:5000/addFollower;
$ curl -i -X DELETE -H 'Content-Type:application/json' -d '{"usernameAPI":"om", "usernameFollowingAPI":"ankita"}' http://localhost:5000/removeFollower;

Follow the similar steps for Timeline Service as well.
