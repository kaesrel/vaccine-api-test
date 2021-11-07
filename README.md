# WCG API TEST

## Instructions:

The test is usable only for the logging branch version of the WCG project, since it is much more stable than the current WCG master branch version.


### Clone the Government-APIs repository

Clone the [Government-APIs repository](https://github.com/WorldClassProgrammers/Government-APIs)
```
git clone https://github.com/WorldClassProgrammers/Government-APIs.git
```


Go into the Government-APIs repository:
```
cd Government-APIs
```

Make sure to checkout out to the logging branch with this command:
```
git checkout logging
```

Follow the [instructions](https://github.com/WorldClassProgrammers/Government-APIs/blob/master/README.md) in the Government-APIs repository in order to run the app.


### Clone and Run the wcg-api-test

After finishing the instruction, go out of the Government-APIs directory, then clone this repository.
```
cd ..
git clone https://github.com/kaesrel/wcg-api-test.git
```

If you do not have the python-decouple module installed, then run this.
```
pip install python-decouple
```

Create a file name `.env`, then configure it with these values:
```
BASE_URL=http://127.0.0.1:5000
```

After that, run the test using this command:
```
python3 -m unittest test_reservation
```


