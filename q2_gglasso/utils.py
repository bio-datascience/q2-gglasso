import numpy as np
import pandas as pd
from scipy import stats
import warnings


def flatten_array(x):
    """
    Flatten a NumPy array.

    Parameters:
    - x: The input array.

    Returns:
    - np.ndarray: A flattened version of the input array.
    """
    x = np.array(x)
    x = x.flatten()
    return x


def list_to_array(x=list):
    """
    Convert a list to a NumPy array.

    Parameters:
    - x (list): The input list.

    Returns:
    - np.ndarray or scalar: A NumPy array if the list has more than one element, or a scalar if it has only one element.
    """
    if isinstance(x, list):
        x = np.array(x)

        if len(x) == 1:
            x = x.item()
    return x


def numeric_to_list(x):
    """
    Convert a numeric value or None to a list.

    Parameters:
    - x (int, float, or None): The input value.

    Returns:
    - list: A list containing the input value. If the input is already a list or None, it is returned as is.
    """
    if (isinstance(x, (int, float))) or (x is None):
        x = [x]
    return x

def if_equal_dict(a, b):
    """
    Check if the values for each key in two dictionaries are equal.

    Parameters:
    - a (dict): The first dictionary.
    - b (dict): The second dictionary.

    Returns:
    - bool: True if the values for each key are equal, False otherwise.
    """
    x = True
    for key in a.keys():
        if a[key].all() == b[key].all():
            continue
        else:
            x = False
    return x


def pep_metric(matrix: pd.DataFrame):
    """
        Calculate the Positive Edge Proportion (PEP) metric for a given adjacency matrix.
        The ratio of the number of positive edges to the total number of edges.

        Parameters:
        - matrix (pd.DataFrame): The adjacency matrix representing interactions between nodes.

        Returns:
        - float: The Positive Edge Proportion (PEP) metric, rounded to two decimal places.
    """
    total_edges = np.count_nonzero(matrix) / 2
    positive_edges = np.sum(matrix > 0, axis=0)
    total_positives = np.sum(positive_edges) / 2
    pep_stat = np.round(total_positives / total_edges, 2)
    return pep_stat


def if_2d_array(x=np.ndarray):
    """
    Ensure input array is 2D.

    Parameters:
    - x (numpy.ndarray): The input array.

    Returns:
    - numpy.ndarray: The input array as a 2D array.
    """
    #  if 3d array of shape (1,p,p),
    #  make it 2d array of shape (p,p).
    if x.shape[0] == 1:
        x = x[0, :]
    return x


def if_all_none(lambda1, lambda2, mu1):
    """
        Check if all hyperparameters (lambda1, lambda2, mu1) are None and set default values if needed.

        Parameters:
        - lambda1: The value or list of values for lambda1.
        - lambda2: The value or list of values for lambda2.
        - mu1: The value or list of values for mu1.

        Returns:
        - tuple: A tuple containing updated values for lambda1, lambda2, and mu1.

        If all hyperparameters are None, default values are set and a message is printed.
    """
    if lambda1 is None and lambda2 is None and mu1 is None:
        lambda1 = np.logspace(0, -3, 10)
        lambda2 = np.logspace(-1, -4, 5)
        mu1 = np.logspace(2, -1, 10)

        print("Setting default hyperparameters:")
        print('\tlambda1 range: [%s]' % ', '.join(map(str, lambda1)))
        print('\tlambda2 range: [%s]' % ', '.join(map(str, lambda2)))
        print('\tmu1 range: [%s]\n' % ', '.join(map(str, mu1)))

    return lambda1, lambda2, mu1


def if_model_selection(lambda1, lambda2, mu1):
    """
    Check if model selection is enabled based on the provided lambda and mu values.

    Parameters:
    - lambda1: The value or list of values for lambda1.
    - lambda2: The value or list of values for lambda2.
    - mu1: The value or list of values for mu1.

    Returns:
    - bool: True if model selection is enabled (multiple values for lambda1, lambda2, or mu1), False otherwise.
    """
    lambda1 = numeric_to_list(lambda1)
    lambda2 = numeric_to_list(lambda2)
    mu1 = numeric_to_list(mu1)

    model_selection = True
    if (len(lambda1) == 1) and len(lambda2) == 1 and (len(mu1) == 1):
        model_selection = False

    return model_selection


def get_seq_depth(counts):
    """
    Calculate and scale sequencing depth from count data.

    Parameters:
    - counts (numpy.ndarray or pandas.DataFrame): A 2D array or DataFrame where rows represent features and columns represent samples.

    Returns:
    - numpy.ndarray: Scaled sequencing depth values.

    The sequencing depth is calculated by summing counts across features or samples based on the larger dimension.
    The depth values are then scaled to the range [0, 1].
    """

    p, n = counts.shape
    if p >= n:
        depth = counts.sum(axis=0)
    else:
        depth = counts.sum(axis=1)
    depth_scaled = (depth - depth.min()) / (depth.max() - depth.min())
    return depth_scaled


def get_range(lower_bound, upper_bound, n):
    """
        Generate a logarithmic range of values between lower_bound and upper_bound.

        Parameters:
        - lower_bound (float or None): The lower bound of the range. If None, a default value of 1e-3 is used.
        - upper_bound (float or None): The upper bound of the range. If None, a default value of 1 is used.
        - n (int): The number of values to generate in the logarithmic range.

        Returns:
        - list: A list of n logarithmically spaced values between lower_bound and upper_bound.
          If both lower_bound and upper_bound are None, the list contains a single element [None].

        Example:
            get_range(0, 2, 5)
            [1e-3, 0.01, 0.1, 1.0, 10.0]
        """
    if (lower_bound is None) and (upper_bound is None):
        range = [None]
    else:
        if lower_bound is None:
            lower_bound = 1e-3
        if upper_bound is None:
            upper_bound = 1
        range = np.logspace(np.log10(lower_bound), np.log10(upper_bound), n)
    return range


def get_hyperparameters(lambda1_min, lambda1_max, lambda2_min, lambda2_max, mu1_min, mu1_max,
                        n_lambda1: int = 1, n_lambda2: int = 1, n_mu1: int = 1):
    """
       Generate hyperparameters for a model based on specified ranges.

       Parameters:
       - lambda1_min (float): The minimum value for lambda1.
       - lambda1_max (float): The maximum value for lambda1.
       - lambda2_min (float): The minimum value for lambda2.
       - lambda2_max (float): The maximum value for lambda2.
       - mu1_min (float): The minimum value for mu1.
       - mu1_max (float): The maximum value for mu1.
       - n_lambda1 (int, optional): The number of values to generate for lambda1 (default is 1).
       - n_lambda2 (int, optional): The number of values to generate for lambda2 (default is 1).
       - n_mu1 (int, optional): The number of values to generate for mu1 (default is 1).

       Returns:
       - dict: A dictionary containing model hyperparameters:
         - 'model_selection' (bool): True if multiple values for any hyperparameter, False if all hyperparameters have a single value.
         - 'lambda1' (float or array): The generated values for lambda1.
         - 'lambda2' (float or array): The generated values for lambda2.
         - 'mu1' (float or array): The generated values for mu1.
        """

    lambda1 = get_range(lower_bound=lambda1_min, upper_bound=lambda1_max, n=n_lambda1)
    lambda2 = get_range(lower_bound=lambda2_min, upper_bound=lambda2_max, n=n_lambda2)
    mu1 = get_range(lower_bound=mu1_min, upper_bound=mu1_max, n=n_mu1)

    model_selection = True

    if None in lambda1:
        lambda1 = np.logspace(0, -4, 15)
        warnings.warn("Default values for lambda1 have been used.")
    if None in lambda2:
        lambda2 = np.logspace(-1, -4, 5)
        warnings.warn("Default values for lambda2 have been used.")
    if None in mu1:
        mu1 = np.logspace(2, -1, 10)
        warnings.warn("Default values for mu1 have been used.")

    if (len(lambda1) == 1) and len(lambda2) == 1 and (len(mu1) == 1):
        lambda1 = np.array(lambda1).item()
        lambda2 = np.array(lambda2).item()
        mu1 = np.array(mu1).item()

        model_selection = False

    h_params = {"model_selection": model_selection, "lambda1": lambda1, "lambda2": lambda2, "mu1": mu1}

    return h_params


def get_lambda_mask(adapt_lambda1: list, covariance_matrix: pd.DataFrame):
    """
        Generate a lambda mask based on adaptive lambda values.

        Parameters:
        - adapt_lambda1 (list): A list containing pairs of strings and corresponding lambda values to adapt.
          The strings represent patterns to match in index and column labels of the covariance_matrix.
          The lambda values are applied to the elements in the covariance_matrix that match the patterns.
        - covariance_matrix (pd.DataFrame): The covariance matrix to which adaptive lambda values will be applied.

        Returns:
        - np.ndarray: A masked version of the covariance matrix with adaptive lambda values.
    """

    mask = np.ones(covariance_matrix.shape)
    adapt_dict = {adapt_lambda1[i]: adapt_lambda1[i + 1] for i in range(0, len(adapt_lambda1), 2)}

    mask_df = pd.DataFrame(mask, index=covariance_matrix.index, columns=covariance_matrix.columns)
    for key, item in adapt_dict.items():
        x_ix = mask_df.index.str.endswith(key)
        x_col = mask_df.columns[mask_df.columns.to_series().str.endswith(key)]
        mask_df[x_ix] = float(item)
        mask_df[x_col] = float(item)
        print("ADAPTIVE lambda={0} has been used for:{1}".format(item, x_col))
    lambda1_mask = mask_df.values

    return lambda1_mask


def check_lambda_path(P, mgl_problem=False):
    """
        Check if optimal lambda values are on the edges of their respective intervals.

        Parameters:
        - P: The problem instance containing model selection parameters and statistics.
        - mgl_problem (bool, optional): Indicates whether the problem is a multi-group lasso problem (default is False).

        Returns:
        - bool: True if the optimal lambda values are on the edges of their intervals, False otherwise.

        Warnings:
        - Issues warnings if the optimal lambda values are on the edge of their intervals.

    """
    sol_par = P.__dict__["modelselect_params"]
    lambda1_opt = P.modelselect_stats["BEST"]["lambda1"]
    lambda1_min = sol_par["lambda1_range"].min()
    lambda1_max = sol_par["lambda1_range"].max()

    boundary_lambdas = False

    if lambda1_opt == lambda1_min:
        boundary_lambdas = True
        warnings.warn("lambda is on the edge of the interval, try SMALLER lambda1")

    elif lambda1_opt == lambda1_max:
        boundary_lambdas = True
        warnings.warn("lambda is on the edge of the interval, try BIGGER lambda1")

    if mgl_problem:
        lambda2_opt = P.modelselect_stats["BEST"]["lambda2"]
        lambda2_min = sol_par["lambda2_range"].min()
        lambda2_max = sol_par["lambda2_range"].max()

        if lambda2_opt == lambda2_min:
            boundary_lambdas = True
            warnings.warn("lambda is on the edge of the interval, try SMALLER lambda2")

        elif lambda2_opt == lambda2_max:
            boundary_lambdas = True
            warnings.warn("lambda is on the edge of the interval, try BIGGER lambda2")

    return boundary_lambdas


def normalize(X):
    """
    transforms to the simplex
    X should be of a pd.DataFrame of form (p,N)
    """
    return X / X.sum(axis=0)


def geometric_mean(x, positive=False):
    """
    calculates the geometric mean of a vector
    """
    assert not np.all(x == 0)

    if positive:
        x = x[x > 0]
    a = np.log(x)
    g = np.exp(a.sum() / len(a))
    return g


def log_transform(X, transformation=str, eps=0.1):
    """
    log transform, scaled with geometric mean
    X should be a pd.DataFrame of form (p,N)
    """
    if transformation == "clr":
        assert not np.any(X.values == 0), "Add pseudo count before using clr"
        g = X.apply(geometric_mean)
        Z = np.log(X / g)
    elif transformation == "mclr":
        g = X.apply(geometric_mean, positive=True)
        X_pos = X[X > 0]
        Z = np.log(X_pos / g)
        Z = Z + abs(np.nanmin(Z.values)) + eps
        Z = Z.fillna(0)
    return Z


def zero_imputation(df: pd.DataFrame, pseudo_count: int = 1):
    """
    Perform zero imputation on a DataFrame by adding a pseudo count to zero values and scaling.

    Parameters:
    - df (pd.DataFrame): The input DataFrame with potentially zero values.
    - pseudo_count (int, optional): The pseudo count added to zero values (default is 1).

    Returns:
    - pd.DataFrame: The DataFrame after zero imputation.
    """
    X = df.copy()
    original_sum = X.sum(axis=0)  # sum in a sample (axis=0 if p, N matrix)
    for col in X.columns:
        X[col].replace(to_replace=0, value=pseudo_count, inplace=True)
    shifted_sum = X.sum(axis=0)
    scaling_parameter = original_sum.div(shifted_sum)  # you need to scale as you added 1 to zeros
    X = X.mul(scaling_parameter, axis=1)

    return X


def remove_biom_header(file_path):
    """
    Remove the header line from a BIOM file.

    Parameters:
    - file_path (str): The path to the BIOM file.
    """
    with open(str(file_path), 'r') as fin:
        data = fin.read().splitlines(True)
    with open(str(file_path), 'w') as fout:
        fout.writelines(data[1:])


def calculate_seq_depth(data=pd.DataFrame):
    """
    Calculate and scale sequencing depth from count data.

    Parameters:
    - data (pd.DataFrame): A DataFrame where rows represent samples and columns represent features.

    Returns:
    - pd.DataFrame: A DataFrame containing scaled sequencing depth values.
    """
    x = data.sum(axis=1)
    x_scaled = (x - x.min()) / (x.max() - x.min())
    seq_depth = pd.DataFrame(data=x_scaled, columns=["sequencing depth"])
    return seq_depth


def single_hyperparameters(model_selection, lambda1, lambda2=None, mu1=None):
    """
    Convert hyperparameters to single values if model selection is not enabled.

    Parameters:
    - model_selection (bool): Indicates whether model selection is enabled.
    - lambda1: The value or list of values for lambda1.
    - lambda2: The value or list of values for lambda2 (default is None).
    - mu1: The value or list of values for mu1 (default is None).

    Returns:
    - tuple: A tuple containing single values for lambda1, lambda2, and mu1 if model selection is not enabled.
    """
    if model_selection is False:
        lambda1 = np.array(lambda1).item()
        lambda2 = np.array(lambda2).item()
        mu1 = np.array(mu1).item()
    return lambda1, lambda2, mu1


def to_zarr(obj, name, root, first=True):
    """
        Convert a GGLasso object to a zarr file with a tree structure.

        Parameters:
        - obj: The GGLasso object or dictionary to be converted.
        - name (str): The name to use for the current level in the zarr hierarchy.
        - root (zarr.Group): The root group to create the zarr hierarchy.
        - first (bool, optional): Indicates whether it is the first level (default is True).
    """
    # name 'S' is dedicated for some internal usage in zarr notation and cannot be accessed as a key while reading
    if name == "S":
        name = 'covariance'

    if isinstance(obj, dict):
        if first:
            zz = root
        else:
            zz = root.create_group(name)

        for key, value in obj.items():
            to_zarr(value, key, zz, first=False)

    elif isinstance(obj, (list, set)):
        root.create_dataset(name, data=obj, shape=len(obj))

    elif isinstance(obj, (np.ndarray, pd.DataFrame)):
        root.create_dataset(name, data=obj, shape=obj.shape)

    elif isinstance(obj, (str, bool, float, int)):
        to_zarr(np.array(obj), name, root, first=False)

    elif isinstance(obj, (np.str_, np.bool_, np.int64, np.float64)):
        to_zarr(np.array(obj), name, root, first=False)

    elif isinstance(obj, type(None)):
        pass
    else:
        to_zarr(obj.__dict__, name, root, first=first)


def PCA(X, L, inverse=True):
    """
        Perform Principal Component Analysis (PCA).

        Parameters:
        - X (pd.DataFrame or np.ndarray): The input data.
        - L (np.ndarray): The Laplacian matrix used in PCA.
        - inverse (bool, optional): If True, perform inverse PCA (default is True).

        Returns:
        - tuple: A tuple containing the PCA results:
            - np.ndarray: The projected data.
            - np.ndarray: The loadings matrix.
            - np.ndarray: The eigenvalues.
    """
    sig, V = np.linalg.eigh(L)

    # sort eigenvalues in descending order
    sig = sig[::-1]
    V = V[:, ::-1]

    ind = np.argwhere(sig > 1e-9)

    if inverse:
        loadings = V[:, ind] @ np.diag(np.sqrt(1 / sig[ind]))
    else:
        loadings = V[:, ind] @ np.diag(np.sqrt(sig[ind]))

    # compute the projection
    zu = X.values @ loadings

    return zu, loadings, np.round(sig[ind].squeeze(), 3)


def correlated_PC(data=pd.DataFrame, metadata=pd.DataFrame, low_rank=np.ndarray,
                  corr_bound=float, alpha: float = 0.05):
    """
    Identify and analyze correlated principal components based on Spearman correlation.

    Parameters:
    - data (pd.DataFrame): The input data with features.
    - metadata (pd.DataFrame): The metadata used for correlation analysis.
    - low_rank (np.ndarray): The low-rank matrix for Principal Component Analysis (PCA).
    - corr_bound (float): The absolute correlation threshold for considering a correlation as significant.
    - alpha (float, optional): The significance level for hypothesis testing (default is 0.05).

    Returns:
    - dict: A dictionary containing information about correlated principal components for each metadata column:
        - key (str): The metadata column name.
        - value (dict): Sub-dictionary with information about correlated principal components:
            - "PC j" (str): The j-th principal component.
            - "data" (pd.DataFrame): The data used for analysis.
            - "eigenvalue" (float): The eigenvalue of the principal component.
            - "rho" (float): Spearman correlation coefficient.
            - "p_value" (float): P-value for the correlation test.
    """

    proj_dict = dict()
    seq_depth = calculate_seq_depth(data)
    r = np.linalg.matrix_rank(low_rank)

    for col in metadata.columns:
        df = data.join(metadata[col])
        df = df.dropna()
        print(col, ":", df.shape)

        proj, loadings, eigv = PCA(df.iloc[:, :-1], low_rank, inverse=True)  # exclude feature column :-1

        df = df.join(seq_depth)

        for j in range(0, r):
            spearman_corr = stats.spearmanr(df[col], proj[:, j])[0]
            p_value = stats.spearmanr(df[col], proj[:, j])[1]
            print("Spearman correlation between {0} and {1} component: "
                  "{2}, p-value: {3}".format(col, j + 1, spearman_corr, p_value))

            if (np.absolute(spearman_corr) > corr_bound) and (p_value < alpha):
                proj_dict[col] = {"PC {0}".format(j + 1): proj[:, j],
                                  "data": df,
                                  "eigenvalue": eigv[j],
                                  "rho": spearman_corr,
                                  "p_value": p_value}

    return proj_dict
