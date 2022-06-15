# ZapCapture
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

  <h3 align="center">ZapCapture</h3>

  <p align="center">
    A python program that extracts lightning images/gifs from videos of storms! ⚡
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

Sometimes I like to set up my camera during storms, but watching hours of footage after a lightning storm is time consuming and not very fun. I went to find an existing script to perform this task, and found one written in Python 2 by programmer and mad scientist [Saulius Lukse](https://lukse.lt/uzrasai/2015-05-lightning-strikes-and-python/). I converted the handy script to Python 3, and fit the whole thing into a Jupyter notebook for easy access.

After showing off my cool pictures, people expressed serious interest in running the software themselves. This wraps the project in a GUI and make it easy enough
for stormchasers and tinkerers to use, while adding additional features like gif support and a progress visual.

### Built With

* [Python](https://www.python.org/)
* [OpenCV](https://opencv.org/)
* [Pillow](https://pillow.readthedocs.io/en/stable/)
* [Tkinter](https://docs.python.org/3/library/tkinter.html)
* [imageio](https://pypi.org/project/imageio/)
* [Atom](https://atom.io/)

<!--Project Roadmap -->
## Roadmap
#### V0 ✔️ (See Independent Repository)
* Script in a Jupyter Notebook. ✔️

#### V1 ✔️
* Implement a working GUI that is OS independent. ✔️

#### V2
* Quality of Life Features
 * requirements.txt ✔️
 * Graphics overhaul for less ugly interface ✔️
 * Multi-threading for faster processing ✔️
 * Progress bar ✔️
 * Error handling to give feedback during analysis ✔️
 * Saved file frame/timestamp option ✔️
 * Detection dead-zone ✔️
 * GIF output mode for cool multi-frame lightning ✔️
 * Fix crash after analysis ✔️
 * Windows Installation ✔️



<!-- DESIGN DESCRIPTION -->
## Design

ZapCapture takes a folder full of videos and uses OpenCV to detect differences between footage frames. If the difference exceeds a user-defined threshold, then the image is saved as a PNG. You can tune the detection threshold to suit your individual video; on a ten minute video, ZapCapture can extract less than a hundred frames or several thousand, depending on the threshold. Sequences of frames will also be saved as gif files, so that you can watch strikes happen in slow-motion.

<p align="center">
  <img src="images/LightningAnalyzerGUI.png" alt="GUI design">
</p>



<!-- USING THE SOFTWARE -->
## Instructions

Instructions for V2 coming soon!

<!-- #### Windows 10
 -->
<!-- Download and install the ZapCapture application for Windows. Run the application. -->

<!--
#### Windows 10

Download the assets folder and LightningGUI.exe, and store them in the same place. Simply run the .exe from there! The .exe was never meant to be a long-term
solution, but simply a minimum viable test tool for some of my friends.

#### Linux

Download the assets folder and LightningGUI file, and store them in the same place. You can run the file from command line with

`$ ./LightningGUI`

-->

#### Processing

1. Use the input and output folder buttons to select a folder with lightning videos and an empty folder.
2. Set an appropriate threshold for your videos. The higher the threshold, the faster the process will run and the less output images you will get. You will have to experiment to find the best threshold, but starting high and going lower is the best approach. The default threshold is too high for almost any detections to occur, so you will need to delete a 0 or two for the best results. If you are having trouble, check the csv outputs and pick a threshold value that is higher than the typical detection value.
3. Select a file name convention- frame number or timestamp (seconds-milliseconds format).
4. Finally, click 'Analyze!' and wait a bit. The program will take a few minutes to run. Once analysis is finished, your output folder will contain all of the image and gif files, as well as a csv giving threshold data for each frame on every file.

#### Building

Interested in building ZapCapture on your system? To build ZapCapture, you need to have Python 3.6 or later. Then, use pip to install the requirements.txt file.

`$ python -m pip install -r requirements.txt`

Run LightningGUI.py to analyze some lightning!

<!-- Finally, use pyinstaller to make the file yourself.

`$ cd Downloads/Lightning-Analyzer-GUI `

`$ pyinstaller LightningGUI.py --onefile --icon logo.ico`

Move the `LightningGUI` file out of the `dist` folder and into to `Lightning-Analyzer-GUI` folder to run it. -->


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Liam Plybon - lplybon1@gmail.com

Project Link: [https://github.com/blablabliam/ZapCapture](https://github.com/blablabliam/ZapCapture)

Like it enough to spend money? Don't feel pressured.

<a href="https://www.buymeacoffee.com/Blablabliam" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Hammer" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgments

* [Saulius Lukse](https://lukse.lt/uzrasai/2015-05-lightning-strikes-and-python/)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/blablabliam/ZapCapture.svg?style=for-the-badge
[contributors-url]: https://github.com/blablabliam/ZapCapture/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/blablabliam/ZapCapture.svg?style=for-the-badge
[forks-url]: https://github.com/blablabliam/ZapCapture/network/members
[stars-shield]: https://img.shields.io/github/stars/blablabliam/ZapCapture.svg?style=for-the-badge
[stars-url]: https://github.com/blablabliam/ZapCapture/stargazers
[issues-shield]: https://img.shields.io/github/issues/blablabliam/ZapCapture.svg?style=for-the-badge
[issues-url]: https://github.com/blablabliam/ZapCapture/issues
[license-shield]: https://img.shields.io/github/license/blablabliam/ZapCapture.svg?style=for-the-badge
[license-url]: https://github.com/blablabliam/ZapCapture/blob/master/LICENSE.txt
