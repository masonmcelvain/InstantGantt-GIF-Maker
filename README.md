# About
This project has two scripts:
1. `main.py`: downloads screenshots of your InstantGantt projects nightly 
2. `make_gif.py`: creates a .gif from all downloaded images to show the changes over time. 

This is a selenium script that I used to schedule nightly downloads of his projects. I haven't tested this since the project ended, so the script may no longer work if InstantGantt has changed.

# Installation Instructions

## Install Dependencies
1. Python 3.9
2. GeckoDriver
3. `pip install -r requirements.txt` in your venv

## SetUp & Run
- Add your username and password project_config.ini
- Set a save directory in program_config.ini
- Set your project settings in project_config.ini (see commented out examples)
- Run `main.py` to download an image for each of your projects

### Schedule
- Update the paths in schedule.bat to match the directory you cloned the repo to and your python venv path
- Use task scheduler to run schedule.bat if you'd like to run the file on a schedule

*Note: Due to the file naming convention, only one file can be saved per day. Running the script more than once per day, will overwrite previous runs from that day.*

## Make GIF
- run `make_gif.py`
- Files will be saved to the location specified in `project_config.ini`

