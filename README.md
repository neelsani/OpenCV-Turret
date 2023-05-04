# OpenCV-Turret

This project implements an object detection model to detect and track humans with a servo motor and  nerf gun.


## Setup (python)

First use the package manager [pip](https://pip.pypa.io/en/stable/) (python 3.8.0) to install the requirements.

```bash
python3 -m pip install -r requirements.txt
```
Next you will need to install [torch](https://pytorch.org/get-started/locally/) for python and optionally gpu. Note: This project was run on a CUDA environment. See personEngine.py
## Setup (arduino)
### Parts
You will need three [MG996R](https://www.digikey.com/en/htmldatasheets/production/5014637/0/0/1/mg996r.html) servos, one [laser diode](https://www.amazon.com/Alinan-Sensor-Non-Modulator-Receiver-Transmitter/dp/B09TP51ZTJ/ref=asc_df_B09TP51ZTJ/?tag=hyprod-20&linkCode=df0&hvadid=598374577587&hvpos=&hvnetw=g&hvrand=2694827591441063411&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9052206&hvtargid=pla-1719263843176&psc=1), one small [nerf gun](https://www.amazon.com/Nerf-N-Strike-Elite-Jolt-Blaster/dp/B01HEQHXE8), an [arduino](https://store.arduino.cc/products/arduino-uno-rev3), a [36W power supply](https://www.amazon.com/dp/B078LSVVTB?)  at 6v, and a 30fps webcam I [used](https://www.amazon.com/Microphone-Streaming-Vitade-682H-Conferencing/dp/B086QT9T13) but really any webcam thats 30fps.  
### Mounting

Put one servo upright and mount another servo sideways on the gear of the first to create a pitch and yaw setup. Mount the webcam on the top and the laser diode on the top of the webcam. Then hot glue the nerf gun to the side of the setup so it moves with the webcam. Then Finally mount the third servo to the trigger of the nerf gun.
Here is a photo:


<img src="https://github.com/neelsani/OpenCV-Turret/blob/master/images/one.jpg?raw=true"  width="300" height="300">
### Pinout
| Part  | Pinout |
| ------------- | ------------- |
| Yaw Servo  | gnd to arduino ground and negative of power supply, vcc to positive of power supply, signal to pin 9  |
| Pitch Servo  | gnd to arduino ground and negative of power supply, vcc to positive of power supply, signal to pin 10  |
| Trigger Servo  | gnd to arduino ground and negative of power supply, vcc to positive of power supply, signal to pin 11  |
| Laser Diode  | gnd to arduino ground, signal to pin 13  |

This project makes use of the pyfirmata library in arduino and python. For this project in the arduino ide simply uplaod the Standard Firmata sketch and that will be all. 
## Usage
For human tracking
```bash
python3 humanTrack.py:

```
For color tracking after you run colorTrack.py simply drag and select a portion of the screen with somewhat uniform color. Then the program will start to track the biggest contour of that color. 
```bash
python3 colorTrack.py

```
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)