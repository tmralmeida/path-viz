# path-viz
Visualization of trajectories based on CSV datasets.
[under construction]


## Status:

- Supported datasets
    - [x] [atc](http://www.irc.atr.jp/crest2010_HRI/ATC_dataset/)
    - [ ] [sCREEN](https://vrai.dii.univpm.it/content/screen-dataset)
- Features
    - [x] path visualization
    - [ ] heading angle

## Arguments:

| Argument Name      |   Type   |    Default    | Additional Info                         |
| ------------------ | :------: | :-----------: | --------------------------------------- |
| --path             |  `str`   |    ------     | Path for the CSV file                   |
| --ds               |  `str`   |    `atc`      | Name of the dataset [`atc`, `screen`]   |
| --n_trajectories   | `int`    |    `1`        | Number of trajectories to show          |
| --draw             | ------   |    ------     | Draw path                               |
| --no_draw          | ------   |    ------     | Only scattered visualization            |


## Example:
```
python main.py --path ../atc-tracking-part1/atc-20121024.csv --draw -nt 6
```

[First Video](https://www.youtube.com/watch?v=SxBLP2oAiGc&list=PL8k82WSQRJKz3dgyfyH0HgmMplfczbxO6&index=3)