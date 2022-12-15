# TicTacToe AI

This project implements basic game of TicTacToe with size 3x3. Current version offers 3 opponent types: Human, MiniMax and AI.

## Players

| Name    | Move is determined by              | Opponent |Trainable* |
|---------|------------------------------------|----------|------------
| Human   | clicking on field with mouse       | 🗸        | ⨉ |
| Random  | pseudorandom number genrator       | ⨉        | 🗸 |
| MiniMax | MiniMax algorithm                  | 🗸        | 🗸 |
| AI      | neural network                     | 🗸        | 🗸 |

\*Type can be used to train model.

## `model_maker.py`

In order to use "AI Player" you have to create and train a model. To simplify this action project contains `model_maker.py` script, which provides basic GUI to generate data, create and train model. It cam be also used to train existing model.

![image](https://user-images.githubusercontent.com/69765321/207975207-503a9f83-b2d4-4740-aaf6-694b41486840.png)

- Generate data - generate and add data to memory
- Dump data     - Removes data from memory
- Train current model   - Trains `model.h5` with data from memory
- Train new model - Creates new `model.h5` or overwrites current

## `main.py`

In order to run the game you have to create model or import model. Then run script `main.py`.

You will see following window:

![image](https://user-images.githubusercontent.com/69765321/207975010-e9ac96cd-29f7-496e-8b94-ed2f15c141a6.png)

After running all games or closing game, window with score is shown.

![image](https://user-images.githubusercontent.com/69765321/207976054-486f2aee-19b0-4cf9-a494-6e0019382902.png)

