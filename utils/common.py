import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from IPython.display import clear_output
from utils.screen import convert_date
import sys
import yaml
import os
from PIL import Image

def get_df(fp, ds = "atc"):
    """ Return the dataframe according to the respective dataset

    Args:
        fp (str): Path of the CSV file
        ds (str, optional): Dataset. Defaults to "atc"
    """
    if ds == "atc":
        col_tit = ["timestamp", 
                   "tag_id", 
                   "x", "y", "z", 
                   "velocity",
                   "angle of motion", 
                   "facing angle"]
        df = pd.read_csv(fp, names = col_tit)
    elif ds in ["edeka", "globus", "aldi", "rewe"]:
        df = pd.read_csv(fp, delimiter=";")
        df["timestamp"] = df["time"].apply(convert_date)
        df = df.drop_duplicates(subset = ["tag_id", "time", "timestamp"])
    else:
        raise ValueError(f"Not prepared for {ds} yet")
    return df

class AnimTraj():
    def __init__(self, df, n_p, dataset_name):
        self.df = df # main dataframe
        self.n_traj = n_p # number of trajectories to plot
        self.ds_n = dataset_name
        self.colors = ["black", "green", "red", "blue", "yellow", "pink", "brown", "darkgray", "preu"] #https://matplotlib.org/stable/gallery/color/named_colors.html
        
        if self.ds_n in ["edeka", "rewe", "aldi", "globus"]:
            curr_path = os.path.abspath(os.path.dirname("cfg"))
            with open(os.path.join(curr_path, "cfg/params.yaml")) as file:
                ps = yaml.safe_load(file)
            self.xmin_map, self.xmax_map, self.ymin_map, self.ymax_map = ps[self.ds_n]
        
    def __sample_ids(self):
        un_ts = self.df["timestamp"].unique() # get different timestamps
        print(f"Df composed of {len(un_ts)} different timestamps. Sampling one...")
        ts = random.choice(un_ts) # radomly sampling one timestamp
        print(f"Timestamp {ts} sampled randomly!")
        ts_ds = self.df[self.df["timestamp"] == ts] # getting all trajectories related to this timestamp
        
        if self.n_traj > ts_ds.shape[0]:
            raise RuntimeError(f"There are no {self.n_traj} different trajectories in this timestamp. Run Again")
        
        print(f"There are {ts_ds.shape[0]} different trajectories in this timestamp. Sampling {self.n_traj}...")
        p_ids = random.sample(ts_ds.tag_id.tolist(), self.n_traj)
        print(f"Plotting trajectories from {p_ids}...")
        return p_ids, ts
    
    def __sample_parwiseids(self):
        return 



    def __get_maxtrajinfo(self, df):
        return df.tag_id.value_counts().max(), df.tag_id.value_counts().idxmax()
    
    
    def __reshape_traj(self, coords, max_traj):
        for c in range(len(coords)):
            if coords[c].shape[0] != max_traj:
                last_idx, last_val = coords[c].shape[0], coords[c][-1, :]
                coords[c] = np.resize(coords[c], (max_traj, coords[c].shape[1]))
                coords[c][last_idx-1:, :] = last_val
        return coords
        
    def __get_axeslim(self, threshold = 500):
        x_min = self.df["x"].min() - threshold
        y_min = self.df["y"].min() - threshold 
        x_max = self.df["x"].max() + threshold 
        y_max = self.df["y"].max() + threshold
        return (x_min, y_min, x_max, y_max)
        
    def __pre_proctrajs(self):
        if self.ds_n == "atc":
            cols = ["timestamp", "x", "y", "z", "facing angle"]
        elif self.ds_n in ["edeka", "globus", "aldi", "rewe"]:
            cols = ["timestamp", "x", "y"]
        p_ids, ts = self.__sample_ids() # sampling ids
        self.p_df = self.df.loc[(self.df["timestamp"] >= ts) & (self.df["tag_id"].isin(p_ids))].sort_values(by="timestamp") # df with the target trajectories
        grouped = self.p_df.groupby(self.p_df.tag_id) # target group
        
        coords = []
        for i in range(self.n_traj):
            p = grouped.get_group(p_ids[i])
            coords.append(p[cols].values)
        max_traj, max_id =  self.__get_maxtrajinfo(self.p_df) # get size of the max traj and the respective id
        n_coords = self.__reshape_traj(coords, max_traj) # reshape smaller trajs to have the same max shape
        return n_coords, max_traj, p_ids
        
    def save(self):
        self.p_df.to_csv(f"{self.ds_n}_{self.n_traj}.csv")
    
    def plot(self, draw_path = False, grid = False, map_path = None):
        coords, max_traj, p_ids = self.__pre_proctrajs()
        x_min, y_min, x_max, y_max = self.__get_axeslim() # axes limits

        plt.ion()
        plt.plot()
        if map_path is not None:
            img = Image.open(map_path)
            plt.imshow(img, extent=[self.xmin_map, self.xmax_map, self.ymax_map, self.ymin_map]);
        for i in range(max_traj):
            plt.clf()
            if map_path is not None:
                plt.imshow(img, extent=[self.xmin_map, self.xmax_map, self.ymax_map, self.ymin_map]);
            else:
                plt.xlim([x_min, x_max]);
                plt.ylim([y_min, y_max]);
            plt.xlabel("x[mm]");
            plt.ylabel("y[mm]");
            if grid ==True:
                plt.grid();
            for p in range(self.n_traj):
                plt.title(f"{self.n_traj} trajectories sampled from {self.ds_n} dataset at {coords[p][i, 0]}");
                if draw_path:
                    plt.plot(coords[p][:i, 1], coords[p][:i, 2], linewidth = 3, label= f"id#{p_ids[p]}", c=self.colors[p])
                else:
                    plt.scatter(coords[p][i, 1], coords[p][i, 2], s = 20, label= f"id#{p_ids[p]}", c=self.colors[p])
                if self.ds_n == "atc":
                        plt.arrow(coords[p][i, 1], coords[p][i, 2], 1.5*(np.cos(coords[p][i, 4])), 1.5*(np.sin(coords[p][i, 4])), width = 300, length_includes_head=True, head_width = 600, color=self.colors[p])
                        
            plt.legend();
            plt.pause(0.00001);
        plt.ioff()
        plt.show()
        

# https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

