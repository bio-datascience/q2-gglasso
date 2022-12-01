from qiime2.plugin import (
    SemanticType,
    Plugin,
    Int,
    Float,
    Range,
    Metadata,
    Str,
    Bool,
    Choices,
    MetadataColumn,
    Categorical,
    List,
    Citations,
    TypeMatch,
    Numeric,
)

from q2_types.feature_table import FeatureTable, Composition


from qiime2.plugin import SemanticType
from q2_types.feature_data import FeatureData


glasso_parameters = {
    "n_samples": List[Int],
    "lambda1_min": List[Float],
    "lambda1_max": List[Float],
    "lambda2_min": List[Float],
    "lambda2_max": List[Float],
    "n_lambda1": Int,
    "n_lambda2": Int,
    "lambda1_mask": List[Float],
    "latent": Bool,
    "non_conforming": Bool,
    "group_array": List[Int],
    "mu1": List[Float],
    "reg": Str
}