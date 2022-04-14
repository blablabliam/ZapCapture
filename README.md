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
themselves. This will wrap the project in a handsome GUI and make it easy enough
for stormchasers and tinkerers to use.

### Built With

* [Python 3.8.13](https://www.python.org/)
* [Anaconda](https://www.anaconda.com/)
* [OpenCV](https://opencv.org/)
* [Pillow](https://pillow.readthedocs.io/en/stable/)
* [Tkinter](https://docs.python.org/3/library/tkinter.html)


<!--Project Roadmap -->
## Roadmap
#### V0 ✔️ (See Independent Repository)
* Implement a working script in a Jupyter Notebook.

#### V1
* Implement a working GUI that is OS independent.

#### V2
* Quality of Life Features
 * Graphics overhaul for less ugly interface
 * Auto-Threshold button to set the threshold on new videos



<!-- DESIGN DESCRIPTION -->
## Design

Currently, the notebook takes a video and uses OpenCV to extract frames and detect a difference between frames. If the difference exceeds the threshold, then the image passes and is saved as a jpg. You can tune the threshold to suit your individual video; on a ten minute video, this program can extract less than a hundred frames or several thousand, depending on the threshold.

Future design should be a standalone program, so that stormchasers don't have to wrangle with software as much.

<!-- USING THE SOFTWARE -->
## Instructions

First, create a new environment in Anaconda and activate it. Install libopencv, opencv, py-opencv, and pillow to the new environment.

Next, create a folder with a lightning video inside; this folder will be filled with images by the lightning frame extractor.

Then, open the lightning extractor notebook. Set the filename to match your lightning video filename; on Linux,

```filename = '/home/user/Videos/Camera/lightning.mp4'```

Finally, set an appropriate threshold for your video. On the example video, the optimum threshold is around 500,000; the higher the threshold, the faster the process will run and the less output images you will get. You will have to experiment to find the best threshold, but starting high and going lower is the best approach. Once the threshold is set, run the notebook and wait a bit. The program will take a few minutes to run.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Liam Plybon - lplybon1@gmail.com

Project Link: [https://github.com/blablabliam/Lightning-Analyzer](https://github.com/blablabliam/Lightning-Analyzer)



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
