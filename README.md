# Backend-Services

This is where various scripts and smaller applications are managed, which are used for the communication between the Node and Pepper application. It is part of the work at the AI Transfer Center Bremerhaven as well as part of the bachelor project of Benjamin T. Schwertfeger, Jacob B. Menge and Kristian Kellermann.

## Requirements

- Python (v3.7.1+)

```bash
╰─ python3 --version
Python 3.7.1
```

- pip (or other python package manager)

## Installation

```bash
╰─ git clone https://github.com/ProjectPepperHSB/Backend-Services
```

Every package has its own install script to install the required packages.

```bash
╰─ python3 -m pip intall -r requirements.txt
```

## Includes

- Analysis part
  - Jupyter Notebook with plots etc...
  - Script to generate weekly reports of peppers activity
- Script to create dummy data, which simulates collected data from interactions with the robot
- Script to fetch timetables from the University of Bremerhaven
- Script to fetch menus from University websites

## Todo

- Comment and format mensa stuff
