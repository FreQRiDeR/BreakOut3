<div align="center">
             <img src="/breakout.png" width="500" />
             <h1>BreakOut3</h1>
</div>


BREAKOUT3 WRITTEN IN PYTHON

* A Python based game where you eliminate blocks by hitting them with a ball. 
* For macOS, Debian based Linux.
* NOW SUPPORTS TOUCHSCREEN, MOUSE!
* Uses pygame, pyinstaller to build play.
* To run the project from source, from working directory:

```sh
# Move into project directory
cd ~/Breakout3
# Create Python 3.13 venv. From working directory, run:
python3.13 -m venv venv # your path may vary
# Activate venv
source venv/bin/activate
# Install requirements
pip install -r requirements.txt
# Run python script
breakout3.py
```
* To build app from source yourself:

```sh
# Move into project directory
cd ~/Breakout3
# Create Python 3.* venv. From working directory, run:
python3.13 -m venv venv # your path may vary
# Activate venv
source venv/bin/activate
# Install requirements
pip install -r requirements.txt
# Create the pyinstaller based Application
python -m PyInstaller breakout3.spec
# Open build folder
open /dist/
# To create .deb Linux package, run:
./breakout3_deb.sh
# To install deb, if you wish, run:
sudo dpkg -i breakout3_v1.0.0.deb
```

* Once done, you'll find the application generated at `/dist/BreakOut3.app`

* By FreQRiDeR and Claude (Mostly Claude! LOL)


