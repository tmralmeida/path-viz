# path-viz
Visualization of huamn motion trajectories based on CSV datasets.
[under construction]


## Status

- Supported datasets
    - [x] [atc](http://www.irc.atr.jp/crest2010_HRI/ATC_dataset/)
    - [x] [sCREEN](https://vrai.dii.univpm.it/content/screen-dataset)
- Features
    - [x] path visualization
    - [x] heading angle (atc dataset)
    - [x] save path
    - [x] draw map (sCREEN dataset)


## Arguments

| Argument Name      |   Type   |    Default    | Additional Info                                         |
| ------------------ | :------: | :-----------: | ------------------------------------------------------- |
| --path             |  `str`   |    ------     | Path for the CSV file                                   |
| --dataset          |  `str`   |    `atc`      | Dataset name [`atc`, `edeka`, `globus`, `aldi`, `rewe`] |
| --map_dir          |  `str`   | `dir_to_map`  | Directory for the map image                             |  
| --n_trajectories   | `int`    |    `1`        | Number of trajectories to show                          |
| --draw             | ------   |    ------     | Draw path                                               |
| --no_draw          | ------   |    ------     | Only scattered visualization                            |


## Running

```
python main.py --path ../datasets/atc-tracking-part1/atc-20121024.csv --draw -nt 6
```

```
python main.py --path ../datasets/new_sCREEN/sCREEN\ dataset/globus.txt --dataset globus --n_trajectories 4 --draw 
```

**Note:** always pass the `path` argument along with the respective `ds` name.

To save the path: press `q` key to close the plot window at the end of the visualization and then press `y` key in the terminal.
## Example

`example` folder contains a saved path of one person from the [atc](http://www.irc.atr.jp/crest2010_HRI/ATC_dataset/) dataset.

## Visualization Examples

[First Video](https://www.youtube.com/watch?v=SxBLP2oAiGc&list=PL8k82WSQRJKz3dgyfyH0HgmMplfczbxO6&index=3)

After including the heading angle provided by the [atc](http://www.irc.atr.jp/crest2010_HRI/ATC_dataset/) dataset:

[Second Video](https://www.youtube.com/watch?v=xOOrKYjS69k)