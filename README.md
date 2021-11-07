# WCG API TEST

### Instructions:

The test is usable only for the logging branch version of the WCG project, since it is much more stable than the current WCG master branch version.

Clone the `logging` branch from the [wcg repository](https://github.com/WorldClassProgrammers/Government-APIs)

Follow the instructions in the WCG repository in order to run the app.


After finishing the instruction, clone this repository.
```
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


