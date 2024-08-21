# home_surveillance

## Setup
### Prerequisites
### Installation
1. `git clone ...`
2. `cd home_surveillance`
3. `python -m venv .venv/`
4. `./.venv/Scripts/activate`
5. `pip install`
6. `python app.py`

## Usage

When starting the program, it is important the camera is not moved or that there are any non-static elements in the frame, for example a person. This is so that the background and foreground segmentation will be consistent and so that the motion detection algorithm works as intended