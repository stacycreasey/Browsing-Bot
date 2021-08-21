# Browsing-Bot

<br />
  <h3 align="center">Browsing Bot</h3>

  <p align="center">
    Python-Selenium scripts to simulate human behavior browsing websites, realistic mouse movement, entering passwords, scrolling etc
    <br />
    <a href="https://youtu.be/5giF2ZNZMcs">View Demo</a>
    ·
    <a href="https://github.com/binarydefense/browsingbot/issues">Report Bug</a>
    ·
    <a href="https://github.com/binarydefense/browsingbot/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#purpose-of-project">Purpose of Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
  </ol>
</details>

<!-- PURPOSE OF PROJECT -->
## Purpose of Project

Binary Defense has set up a controlled lab environment that is isolated from any other network to allow threat actors to attack with no repercussions. Allowing threat actors to attack the lab environment gives our team of threat hunters/researchers data to analyze and further use to prevent attacks on our client's infrastructure. 

One of the main things attackers look for as soon as they have access to a network is its size and the activity. If a network is seemingly empty, the threat actor might move on to a target they feel is more worthwhile. To check activity, some malware variants utilize screen capture techniques to see what a person is doing on a machine. This technique is becoming increasingly popular. By creating a script that mimics human activity programmatically, we can simulate the activity without needing real people on the machines.

### Built With

This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [Python](https://www.python.org/)
* [Selenium](https://selenium-python.readthedocs.io/)

Extras

* [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)
* [Bezier](https://pypi.org/project/bezier/)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* Chrome driver
* Selenium
  ```sh
  pip install selenium==4.0.0a6.post2
  ```
* Numpy
  ```sh
  pip install numpy==1.21.1
  ```
  
Extras

* Bezier
  ```sh
  pip install bezier==2021.2.12
  ```
* PyAutoGUI
  ```sh
  pip install pyautogui==0.9.53
  ```
### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/BinaryDefense/BrowsingBot.git
   ```
2. Install prereqs
3. Change path variable in ```main.py``` to local Chrome driver path
4. Edit ```usernamesPasswords.txt``` file and adjust login_info() function for ```wish.py```, ```shein.py```, ```gearbest.py```, and ```aliExpress.py```

