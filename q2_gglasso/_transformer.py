import pandas as pd
import zarr

from q2_gglasso.plugin_setup import plugin
from biom import load_table, parse_table
import q2_gglasso as q2g

@plugin.register_transformer
def _0(data: pd.DataFrame) -> q2g.GGLassoDataFormat:
    ff = q2g.GGLassoDataFormat()
    with ff.open() as fh:
        data.to_csv(fh, sep='\t', index_label='feature1')
    return ff


@plugin.register_transformer
def _1(ff: q2g.GGLassoDataFormat) -> pd.DataFrame:
    table = load_table(str(ff))
    df = table.to_dataframe()
    return df


@plugin.register_transformer
def _3(obj: q2g.solve_problem) -> q2g.GGLassoProblemDirectoryFormat:
    ff = q2g.GGLassoProblemDirectoryFormat()
    zipfile = str(ff.path / "problem.zip")
    store = zarr.ZipStore(zipfile, mode="w")
    root = zarr.open(store=store)
    q2g.to_zarr(obj, "problem", root)
    store.close()
    return ff


@plugin.register_transformer
def _4(ff: q2g.ZarrProblemFormat) -> zarr.hierarchy.Group:
    store = zarr.ZipStore(str(ff), mode="r")
    root = zarr.open(store=store)
    return root

# @plugin.register_transformer
# def _2(ff: GGLassoDataFormat) -> pd.DataFrame:
#     df = pd.read_csv(str(ff), index_col=0, sep='\t')
#     df = df.dropna(axis=1, how='all')
#     new_index = pd.MultiIndex.from_tuples([(str(i), str(j)) for i, j in df.index])
#     df.index = new_index
#     return df


