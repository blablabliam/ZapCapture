# Lightning Analyzer
 A computer vision program to extract lightning strikes! ⚡


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/blablabliam/Lightning-Analyzer-GUI">
    <img src="images/lightning5.jpg" alt="Lightning Strikes!" width="80" height="80">
  </a>

  <h3 align="center">Lightning Key Frame Extraction GUI</h3>

  <p align="center">
    A Jupyter Notebook that extracts lightning images from videos of storms! :lightning:
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href='#roadmap'>Roadmap</a></li>
      </ul>
    </li>
    <li><a href="#design">Design</a></li>
    <li><a href="#instructions">Instructions</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Sometimes I like to set up my camera during storms, but watching hours of footage after a lightning storm is time consuming and not very fun. I went to find an existing script to perform this task, and found one written in Python 2 by programmer and mad scientist [Saulius Lukse](https://lukse.lt/uzrasai/2015-05-lightning-strikes-and-python/). I converted the handy script to Python 3, and fit the whole thing into a Jupyter notebook for easy access. After showing off my
cool result pictures, people expressed serious interest in running the software
themselves. This wraps the project in a 'handsome' GUI and make it easy enough
for stormchasers and tinkerers to use.

### Built With

* [Python](https://www.python.org/)
* [OpenCV](https://opencv.org/)
* [Pillow](https://pillow.readthedocs.io/en/stable/)
* [Tkinter](https://docs.python.org/3/library/tkinter.html)
* [Atom](https://atom.io/)

<!--Project Roadmap -->
## Roadmap
#### V0 ✔️ (See Independent Repository)
* Implement a working script in a Jupyter Notebook.

#### V1 ✔️
* Implement a working GUI that is OS independent.

#### V2
* Quality of Life Features
 * Graphics overhaul for less ugly interface
 * Auto-Threshold button to set the threshold on new videos
 * Multithreading for faster processing speed
 * Error handling to give feedback during analysis



<!-- DESIGN DESCRIPTION -->
## Design

Currently, the program takes a folder full of videos and uses OpenCV to detect differences between frames. If the difference exceeds a user-defined threshold, then the image is saved as a jpg. You can tune the threshold to suit your individual video; on a ten minute video, this program can extract less than a hundred frames or several thousand, depending on the threshold.

<!-- USING THE SOFTWARE -->
## Instructions

#### Windows 10

Download the assets folder and LightningGUI.exe, and store them in the same place. Simply run the exe from there!

#### Linux

Download the assets folder and LightningGUI file, and store them in the same place. You can run the file from command line with

`$ ./LightningGUI`

#### Processing

Use the input and output folder buttons to select a folder with lightning videos and an empty folder. Then, set an appropriate threshold for your videos. On the example video, the optimum threshold is around 500,000; the higher the threshold, the faster the process will run and the less output images you will get. You will have to experiment to find the best threshold, but starting high and going lower is the best approach. Once the threshold is set, click 'Analyze!' wait a bit. The program will take a few minutes to run.

#### Building

Interested in building LightningGUI on your operating system? To build LightningGUI, you need to have Python 3.6 or later. Then, create a virtual environment.

`$ python -m venv LightningVenv`

`$ cd LightningVenv/Scripts`

`$ activate`

Then, use pip to install pillow, opencv, and pyinstaller.

`(LightningVenv)$ pip install pillow opencv-python pyinstaller`

Finally, use pyinstaller to make the file yourself.

`(LightningVenv)$ cd Downloads/Lightning-Analyzer-GUI `

`(LightningVenv)$ pyinstaller LightningGUI.py --onefile --icon logo.ico`

Move the `LightningGUI` file out of the `dist` folder and into to `Lightning-Analyzer-GUI` folder to run it.


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Liam Plybon - lplybon1@gmail.com

Project Link: [https://github.com/blablabliam/Lightning-Analyzer](https://github.com/blablabliam/Lightning-Analyzer)

Like it enough to spend money? Don't feel pressured.

<a href="https://www.buymeacoffee.com/Blablabliam" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Hammer" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgments

* [Saulius Lukse](https://lukse.lt/uzrasai/2015-05-lightning-strikes-and-python/)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/blablabliam/Lightning-Analyzer.svg?style=for-the-badge
[contributors-url]: https://github.com/blablabliam/Lightning-Analyzer/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/blablabliam/Lightning-Analyzer.svg?style=for-the-badge
[forks-url]: https://github.com/blablabliam/Lightning-Analyzer/network/members
[stars-shield]: https://img.shields.io/github/stars/blablabliam/Lightning-Analyzer.svg?style=for-the-badge
[stars-url]: https://github.com/blablabliam/Lightning-Analyzer/stargazers
[issues-shield]: https://img.shields.io/github/issues/blablabliam/Lightning-Analyzer.svg?style=for-the-badge
[issues-url]: https://github.com/blablabliam/Lightning-Analyzer/issues
[license-shield]: https://img.shields.io/github/license/blablabliam/Lightning-Analyzer.svg?style=for-the-badge
[license-url]: https://github.com/blablabliam/Lightning-Analyzer/blob/master/LICENSE.txt
