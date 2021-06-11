import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from IPython.display import clear_output
from utils.screen import convert_date


def get_df(fp, ds = "atc"):
    """ Return the dataframe according to the respective dataset

    Args:
        fp (str): Path of the CSV file
        ds (str, optional): Dataset. Defaults to "atc"
    """
    if ds == "atc":
        col_tit = ["time", 
                   "id", 
                   "x", "y", "z", 
                   "velocity",
                   "angle of motion", 
                   "facing angle"]
        df = pd.read_csv(fp, names = col_tit)
    elif ds == "screen":
        df = pd.read_csv(fp)
        df["time"] = df["time"].apply(convert_date)
        df[["x", "y", "z"]] = df[["x", "y", "z"]].apply(lambda coord : coord*1000) # convert to mm
    else:
        raise ValueError(f"Not prepared for {ds} yet")
    return df

class AnimTraj():
    def __init__(self, df, n_p, dataset_name):
        self.df = df # main dataframe
        self.n_traj = n_p # number of trajectories to plot
        self.ds_n = dataset_name
        self.colors = ["black", "green", "red", "blue", "yellow", "pink", "gold", "darkgray", "preu", "brown"] #https://matplotlib.org/stable/gallery/color/named_colors.html
        
    def __sample_ids(self):
        un_ts = self.df["time"].unique() # get different time stamples
        print(f"Df composed of {len(un_ts)} different timestamps. Sampling one...")
        ts = random.choice(un_ts) # radomly sampling one timestamp
        print(f"Timestamp {ts} sampled randomly!")
        ts_ds = self.df[self.df["time"] == ts] # getting all trajectories related to this timestamp
        
        if self.n_traj > ts_ds.shape[0]:
            raise RuntimeError(f"There are no {self.n_traj} different trajectories in this timestamp. Run Again")
        
        print(f"There are {ts_ds.shape[0]} different trajectories in this timestamp. Sampling {self.n_traj}...")
        p_ids = random.sample(ts_ds.id.tolist(), self.n_traj)
        print(f"Plotting trajectories from {p_ids}...")
        return p_ids
    

    def __get_maxtrajinfo(self, df):
        return df.id.value_counts().max(), df.id.value_counts().idxmax()
    
    
    def __reshape_traj(self, coords, max_traj):
        for c in range(len(coords)):
            if coords[c].shape[0] != max_traj:
                last_idx, last_val = coords[c].shape[0], coords[c][-1, :]
                coords[c] = np.resize(coords[c], (max_traj, coords[c].shape[1]))
                coords[c][last_idx-1:, :] = last_val
        return coords
        
    def __get_axeslim(self, p_df, threshold = 500):
        x_min = self.df["x"].min() - threshold
        y_min = self.df["y"].min() - threshold 
        x_max = self.df["x"].max() + threshold 
        y_max = self.df["y"].max() + threshold
        return (x_min, y_min, x_max, y_max)
        
    def __pre_proctrajs(self):
        if self.ds_n == "atc":
            cols = ["x", "y", "z", "facing angle"]
        elif self.ds_n == "screen":
            cols = ["x", "y", "z"]
        p_ids = self.__sample_ids() # # sampling ids
        p_df = self.df.loc[self.df["id"].isin(p_ids)] # df with the target trajectories
        grouped = p_df.groupby(p_df.id) # target groupped 
        
        coords = []
        for i in range(self.n_traj):
            p = grouped.get_group(p_ids[i])
            coords.append(p[cols].values)
        max_traj, max_id =  self.__get_maxtrajinfo(p_df) # get size of the max traj and the respective id
        n_coords = self.__reshape_traj(coords, max_traj) # reshape smaller trajs to have the same max shape
        return n_coords, max_traj, p_ids
        
    
    def plot(self, draw_path = True):
        coords, max_traj, p_ids = self.__pre_proctrajs()
        p_df = self.df.loc[self.df["id"].isin(p_ids)] # redundant computation
        x_min, y_min, x_max, y_max = self.__get_axeslim(p_df) # axes limits
        plt.ion()
        plt.plot()
        for i in range(max_traj):
            plt.clf()
            plt.title(f"{self.n_traj} trajectories sampled");
            plt.xlim([x_min, x_max]);
            plt.ylim([y_min, y_max]);
            plt.xlabel("x[mm]");
            plt.ylabel("y[mm]");
            for p in range(self.n_traj):
                if draw_path:
                    plt.plot(coords[p][:i, 0], coords[p][:i, 1], linewidth = 3, label= f"id#{p_ids[p]}", c=self.colors[p])
                else:
                    plt.scatter(coords[p][i, 0], coords[p][i, 1], s = 20, label= f"id#{p_ids[p]}", c=self.colors[p])
                if self.ds_n == "atc":
                        plt.arrow(coords[p][i, 0], coords[p][i, 1], 1500*(np.cos(coords[p][i, 3])), 1500*(np.sin(coords[p][i, 3])), width = 300, length_includes_head=True, head_width = 500, color=self.colors[p])
                        
            plt.legend();
            plt.pause(0.00001);
        plt.ioff()
        plt.show()