import os
import argparse  
from utils.common import *


parser = argparse.ArgumentParser(description = "Visualization tool for motion trajectories")

parser.add_argument(
    "--path",
    "-p",
    type=str,
    help="Dataset path",
    required=True
)

parser.add_argument(
    "--dataset",
    "-ds",
    type=str,
    help="Dataset name",
    choices=["atc", "aldi", "rewe", "globus", "edeka"],
    default="atc"
)


parser.add_argument(
    "--map_dir",
    "-mp",
    type = str,
    default="/home/tmr/Documents/PhD/My_PhD/code/datasets/new_sCREEN",
    required = False,
    help = "map png file path"
)


parser.add_argument(
    "--n_trajectories",
    "-nt",
    type=int,
    help="Number of trajectories to visualize",
    default=1
)


parser.add_argument(
    "--draw", 
    dest="draw", 
    action="store_true")

parser.add_argument(
    "--no_draw", 
    dest="draw", 
    action="store_false")

parser.add_argument(
    "--grid", 
    dest="grid", 
    action="store_true")

parser.add_argument(
    "--no_grid", 
    dest="grid", 
    action="store_false")

parser.set_defaults(draw=False, grid=False)
args = parser.parse_args()
mp = None
if args.dataset in ["edeka", "globus", "aldi", "rewe"]:
    mp = os.path.join(args.map_dir, args.dataset + "_map.png")


df = get_df(args.path, args.dataset)
anim = AnimTraj(df, args.n_trajectories, args.dataset)
anim.plot(draw_path=args.draw, grid = args.grid, map_path = mp)

save = query_yes_no("save trajectory?", default="yes")
if save == True:
    anim.save()