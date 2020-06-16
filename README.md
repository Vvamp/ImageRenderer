<!-- Project Badges-->
![Contributors Badge](https://img.shields.io/github/contributors/Vvamp/ImageLoader.svg?style=flat-square)
![Forks Badge](https://img.shields.io/github/forks/Vvamp/ImageLoader.svg?style=flat-square)
![Stars Badge](https://img.shields.io/github/stars/Vvamp/ImageLoader.svg?style=flat-square)
![Issues Badge](https://img.shields.io/github/issues/Vvamp/ImageLoader.svg?style=flat-square)
![License Badge](https://img.shields.io/github/license/Vvamp/ImageLoader.svg?style=flat-square)


# Image Renderer
A simple script that can render raw RGB data into a JPEG image.

## Table of Contents
- [Getting Started](#Getting-Started)
    - [Prerequisites](#Prerequisites)
    - [Installation]("#Installation)
- [Usage](#Usage)
    - [Automatic Options](#Automatic-Options)
    - [Command Line Arguments](#Command-Line-Arguments)
- [Contributing](#Contributing)
- [License](#License)
- [Contact](#Contact)
- [Acknowledgements](#Acknowledgements)

## Getting Started
### Prerequisites
1. [Python](https://www.python.org/)
2. Pillow `pip install Pillow`
3. PySerial `pip install pyserial`

### Installation
Simply clone this project somewhere you like and you're done!

## Usage
### Automatic Options
Simple run `python render.py` in a terminal opened from the folder you cloned to.  
This will run you through the required options.

### Command Line Arguments
There are a lot of command line arguments you can pass.
For example: `python render.py -h` shows all the available command line arguments and their usage.  
The command `python render.py -o my_image.jpg` exports the rendered image into a file name 'my_image.jpg'.

**See `python render.py -h` for a list of commands**
## Tests
You can test the code by running `python render.py --path tests/test.txt -o tests/test.jpg --findx --findy -q`.
This should generate an image file within the tests folder called 'test.jpg' and should look identical to the 'test-target.jpg'.
![test-target.jpg](tests/test-target.jpg)


## Contributing
1. Fork the project
2. Create a feature branch: `git checkout -b feature/<FeatureName>`
3. Make your changes
4. Commit your changes: `git commit -m "<Describe your changes"`
5. Push to the branch: `git push origin feature/<FeatureName>`
6. Open a pull request

## License
Distributed under the GNU General Public License V3.  
See `LICENSE` for more details.

## Contact
Vincent van Setten - [@Vvamp](https://github.com/Vvamp) - [school@vincentvansetten.com](mailto:school@vincentvansetten.com)  
Project: [Image Renderer](https://github.com/Vvamp/ImageRenderer)

## Acknowledgements
- [Hogeschool Utrecht](https://www.hu.nl/)
- [Shields.io](https://https://shields.io/)
- [Readme Template](https://github.com/othneildrew/Best-README-Template)