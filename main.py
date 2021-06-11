import argparse  
from utils.common import get_df, AnimTraj


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
    choices=["atc", "screen"],
    default="atc"
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

parser.set_defaults(draw=False)

args = parser.parse_args()
df = get_df(args.path, args.dataset)
anim = AnimTraj(df, args.n_trajectories, args.dataset)
anim.plot(draw_path=args.draw)
