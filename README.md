# StintFlow

StintFlow helps Le Mans Ultimate racers keep track of their sessions and plan their races. It runs on your desktop and provides:

- automatic logging of stints while you drive
- strategy tables to plan and compare how to approach the race, both before and during an event
- real‑time integration with the LMU game so you can see live data on your screen
- a history of past races stored on your computer for review and analysis

## Quick Start

If you're a regular user or player and just want to try the software, head to the [Releases page](https://github.com/KSiig/StintFlow/releases) and download the latest build for Windows. No programming knowledge is required – just unzip and run the `StintFlow` executable.

For developers or anyone building from source, use the commands below:

```powershell
git clone https://github.com/yourusername/StintFlow.git
cd StintFlow
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

> Make sure you have Python 3.14 installed and a MongoDB instance running locally. The LMU game is optional but required for live shared-memory data.

## Run from Source

1. **Prerequisites**
   - Python 3.14
   - MongoDB (local or remote)
   - (Optional) LMU simulator/game for shared memory

2. **Installation steps**
   - Clone the repository.
   - Install dependencies with `pip install -r requirements.txt`.
   - Launch the application: `python main.py`.

3. **Configuration**
   - User settings are stored in `%APPDATA%\StintFlow` (Windows). See `tools/load_user_settings.py` for details.

## Build Executable

The project includes a PyInstaller spec file (`StintFlow.spec`). To build a standalone executable on Windows:

```powershell
pyinstaller StintFlow.spec
```

The generated executable will appear in the `dist\StintFlow` directory.

## Features

![Config options and table overview](docs\screenshots\config_options.png)
- Track race sessions and stints

![Strategies overview](docs\screenshots\strategies.png)
- Calculate optimal strategies
- LMU shared memory integration for real-time data
- Modular architecture with independent processor subprocesses
- MongoDB backend for persistence

For more information on the `stint_tracker` processor, see `processors/stint_tracker/README.md`.

## License

This project is released under the terms of the [LICENSE](LICENSE) file.

## Contact

For questions or support, contact **Kasper Siig** at <kasper@siig.tech>.
