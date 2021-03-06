# Aphasia-project

**Description**

Patients that suffer from Aphasia have difficulty comprehending and/or formulating language. 
The cause is usually brain damage in the language center. Recovery from Aphasia is usually never 100%, and rehab can take years but does help the patients. 
Regardless, having Aphasia is usually very stressful for the patients even during rehabilitation sessions. Specialists from the Rijndam rehabilitation institute in Rotterdam treat patients that suffer from Aphasia. 
Their impression is that the stress experienced by patients may be amplified by human-human interaction in which the patients experience the 'embarrassment' of not being able to communicate correctly. 
Possibly, the rehabilition stress can be reduced by having patients do exercises on a computer rather than to talk to a person. For this project the first goal is to see if we can properly translate what Aphasia patients say to text and identify where they likely make mistakes in their language.

# Installation guide

First perform the following steps, see below
1. Create a new folder and name it 'Git'

2. Download and install Git from the link below<br>
[MAC] : https://git-scm.com/download/mac <br>
[WINDOWS] : https://git-scm.com/download/win

2. Enter the following on the terminal / command prompt (This will download de repo)<br>
2.1 cd <i>PATH TO YOUR FOLDER</i> <br>
2.2 git clone https://github.com/ciCciC/Aphasia-project.git


**MAC**
1. Download and install PyCharm<br>
https://www.jetbrains.com/pycharm/

2. Download and install the latest Python version<br>
https://www.python.org/downloads/mac-osx/

3. Install Pip only if you dont have it **(Pip is mostly installed after installing Python)**<br>
3.1 Check on your terminal if you have pip installed, see below<br>
pip -V<br>
3.2 Download and install Pip<br>
Download get-pip.py from <a href="https://pip.pypa.io/en/stable/installing/">HERE</a> to a folder on your computer. Open terminal and navigate to the folder containing get-pip.py. Then run python get-pip.py. This will install pip.

**WINDOWS**
1. Download and install PyCharm<br>
https://www.jetbrains.com/pycharm/

2. Download the latest Python version<br>
https://www.python.org/downloads/windows/

3. Install Pip only if you dont have it **Pip is mostly installed after installing Python**<br>
3.1 Check on your command prompt if you have pip installed, see below<br>
pip --version<br>
3.2 Download and install Pip<br>
Download get-pip.py from <a href="https://pip.pypa.io/en/stable/installing/">HERE</a> to a folder on your computer. Open a command prompt window and navigate to the folder containing get-pip.py. Then run python get-pip.py. This will install pip.

**After installing PyCharm, Python and Pip please see below**

1. Install Google Cloud Speech from the **terminal of your PyCharm SDK**<br>
pip install --upgrade google-cloud-speech <br>

2. For being able to load mp3 EG for converting to .WAV or .FLAC extension we need the following<br>
- Windows, download and install<br>
https://ffmpeg.zeranoe.com/builds/ <br>

- Mac, download homebrew and install<br>

brew install ffmpeg --with-libvorbis --with-sdl2 --with-theora

[Test] ONLY FOR KORAY !<br>
create a virtual environment<br>
cd project_folder<br>
virtualenv <your-env-NAME><br>
source <your-env-NAME>/bin/activate<br>
<your-env-NAME>/bin/pip install google-cloud-storage<br>
<your-env-NAME>/bin/pip install google-cloud-speech<br>
