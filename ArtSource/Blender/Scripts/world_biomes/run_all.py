"""run_all.py — build all sub-folder assets."""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_ROOT = os.path.normpath(os.path.join(_HERE, '..'))
if _SCRIPTS_ROOT not in sys.path:
    sys.path.insert(0, _SCRIPTS_ROOT)

from world_biomes.fossil_sky.run_all import run_all as run_fossil_sky
from world_biomes.glassroot_forest.run_all import run_all as run_glassroot_forest
from world_biomes.gravity_well.run_all import run_all as run_gravity_well
from world_biomes.inner_sea.run_all import run_all as run_inner_sea
from world_biomes.mantle_garden.run_all import run_all as run_mantle_garden


def run_all():
    run_fossil_sky()
    run_glassroot_forest()
    run_gravity_well()
    run_inner_sea()
    run_mantle_garden()


if __name__ == "__main__":
    run_all()
