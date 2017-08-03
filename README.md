# game-of-life
John Conway's Game of Life in Tkinter

## About
Rules of Conway's Game of Life:
1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

See [Wikipedia Page](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

## Usage
To run this program use

    python main.py

### Controls
Once run, you can control the game using the mouse and the menu buttons.

Mouse:
* Leftclick and drag mouse to move screen
* Ctrl+leftclick to place cell at mouse position
* Rightclick to erase cells

Menu:
* Presets - load a preset onto the canvas (i.e. glider gun)
* Delay - change the delay between frames
* Step - change the frame step to display only every few frames
* Randomize - place cells randomly over a certain range
* Start/Pause - starts processing, stops processing
* Reset - Clear cells

### Creating Presets
To create presets, run presetMaker.py.

You can change the GRID and TILESIZE hyperparameters to make differently sized presets.

Leftclick to place, Rightclick to erase, and Enter to print the array, which can be used to add the new preset to the presets.py file dictionary.

## Future Developments
In the future, I plan to add the following features:

* More presets to choose from
* Faster processing
* More user-friendly preset creation
