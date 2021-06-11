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
    - [ ] draw map (sCREEN dataset)


## Arguments

| Argument Name      |   Type   |    Default    | Additional Info                         |
| ------------------ | :------: | :-----------: | --------------------------------------- |
| --path             |  `str`   |    ------     | Path for the CSV file                   |
| --ds               |  `str`   |    `atc`      | Name of the dataset [`atc`, `screen`]   |
| --n_trajectories   | `int`    |    `1`        | Number of trajectories to show          |
| --draw             | ------   |    ------     | Draw path                               |
| --no_draw          | ------   |    ------     | Only scattered visualization            |


## Running

```
python main.py --path ../atc-tracking-part1/atc-20121024.csv --draw -nt 6
```
**Note:** always pass the `path` argument along with the respective `ds` name.

After the trajectory finishing, we can save the model by first pressing `q` key to close the plot window and then by answering to the prompted question.
## Example

`example` folder contains a saved path of one person from the [atc](http://www.irc.atr.jp/crest2010_HRI/ATC_dataset/) dataset.

[First Video](https://www.youtube.com/watch?v=SxBLP2oAiGc&list=PL8k82WSQRJKz3dgyfyH0HgmMplfczbxO6&index=3)