# EEG-Brainwave-Music
Windows implementation of brainwave powered music synthesizer written in Python and Clojure.
Current version uses piano notes to represent relative changes in brainwaves amplitudes. 
Meditation value is used to schedule delay between notes.
Python app can save EEG data into csv file. (Turned on by default)

Requirements:
* [PyBluez](http://code.google.com/p/pybluez/), see their [documentation](http://code.google.com/p/pybluez/wiki/Documentation) for installation instructions.
* [Python Mindwave Mobile] (https://github.com/robintibor/python-mindwave-mobile) one way to install is using ``` pip install git + https://github.com/```
* [Overtone] (https://github.com/overtone/overtone/wiki) [installation] (https://github.com/overtone/overtone/wiki/Installing-overtone)
* [SuperCollider] (http://supercollider.github.io/download)
* [Clojure] (https://clojure.org) and [Leiningen] (https://github.com/technomancy/leiningen/#installation)


Inspired by Joseph Wilk's "Sounds of the Human Brain" post:
http://blog.josephwilk.net/clojure/sounds-of-the-human-brain.html