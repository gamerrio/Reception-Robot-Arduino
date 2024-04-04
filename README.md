# Reception-Robot_Arduino

<p align='center'>
<img src='https://forthebadge.com/images/badges/built-with-love.svg'> <img src='https://forthebadge.com/images/badges/made-with-python.svg'><br>
<img src='https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white'><img src='https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white'><br>
<img src='https://img.shields.io/github/license/gamerrio/discord-chat-bot?style=for-the-badge'><br>
<img src='https://img.shields.io/badge/os-windows-green'>
<img src='https://img.shields.io/badge/os-linux-green'>
<img src='https://img.shields.io/badge/os-mac-green'></p>

***
### A Reception Chat Bot Made using Arduino and TinyLlama (Transformers)
<br>

> ## **Usage:**
1. Clone this repository
```
git clone https://github.com/gamerrio/Reception-Robot-Arduino.git
cd Reception-Robot-Arduino
```
2. Create a python virtual environment.
```
echo "Create Virtual Environment"
python -m venv myenv
echo "Activate Environment"
source myenv/bin/activate
```
3. Install packages.
```
echo "Install packages"
pip install -r requirements.txt
```
4. create a .env file that should look like: <br>
Find your Access Key Here : [picovoice.ai](https://picovoice.ai/)

```
ACCESS_KEY="" 
KEYWORDS="terminator"  
```
1. run the python file
```
python3 Face_Detect.py
python3 Flask_Server.py
python3 Wake_Client.py
```
> ## Preview:
> ![Robot](./Robot.jpg)

> ## Wiring:
- Servo (Up/Down) 
  - Servo Gnd -> Gnd
  - Servo VCC -> 5v
  - Servo Signal -> D6
- Servo (Left/Right) 
  - Servo Gnd -> Gnd
  - Servo VCC -> 5v
  - Servo Signal -> D5
- Servo (rotate left/right) 
  - Servo Gnd -> Gnd
  - Servo VCC -> 5v
  - Servo Signal -> D7

## Please Leave A Star :star2: