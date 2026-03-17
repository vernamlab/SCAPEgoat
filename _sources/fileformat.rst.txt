Custom File Framework
==================
The file framework is split into three separate classes.

.. class:: FileParent

    .. method:: __init__(self, name: str, path: str, existing: bool = False):

        Initialize FileFormatParent class. Creates the basic file structure including JSON metadata holder. If the file
        already exists it simply returns a reference to that file. To create a file named "ExampleFile" in your downloads
        directory set the name parameter to `name="ExampleFile` and the path to `path="C:\\users\\username\\\desktop`. The
        path needs to be structured as shown with double back slashes.

        :param name: The name of the file parent directory
        :type name: str
        :param path: The path to the file parent.
        :type path: str
        :param existing: whether the file already exists
        :type existing: bool
        :returns: None

    .. method:: update_metadata(self, key: str, value: any) -> None:

        Update file JSON metadata with key-value pair

        :param key: The key of the metadata
        :type key: str
        :param value: The value of the metadata. Can be any datatype supported by JSON
        :type value: any
        :returns: None


    .. method:: read_metadata(self) -> dict:

        Read JSON metadata from file

        :returns: The metadata dictionary for the FileParent object
        :rtype: dict

    .. methood:: add_experiment(self, name: str) -> 'Experiment':

        Adds a new experiment to the FileParent object

        :param name: The desired name of the new experiment
        :type name: str
        :returns: The newly created Experiment object
        :rtype: Experiment

    .. method:: get_experiment(self, experiment_name: str) -> 'Experiment':

        Get an existing experiment from the FileParent.

        :param experiment_name: The name of the requested experiment
        :type experiment_name: str
        :returns: The requested experiment. None if it does not exist.
        :rtype: Experiment. None if not found.
        

    .. method:: delete_file(self) -> None:

        Deletes the entire file. Confirmation required.

        :returns: None

    .. method:: delete_experiment(self, experiment_name: str) -> None:

        Deletes an experiment and all of its datasets from a FileParent. Confirmation Required.

        :param experiment_name: The name of the experiment
        :type experiment_name: str
        :returns: None

    .. method:: query_experiments_with_metadata(self, key: str, value: any, regex: bool = False) -> list['Experiment']:

        Query all experiments in the FileParent object based on exact metadata key-value pair or using regular expressions.

        :param key: The key to be queried
        :type key: str
        :param value: The value to be queried. Supply a regular expression if the `regex` parameter is set to true. Supplying
                        a value of "*" will return all experiments with the `key` specified in the key parameter.
        :type value: any
        :returns: A list of queried experiments
        :rtype: list['Experiment']


.. class:: Experiment

    .. method:: __init__(self, name: str, path: str, file_format_parent: FileParent, existing: bool = False, index: int = 0, experiment: dict = None):

        Creates an Experiment object. Do not call this constructor. Please use `FileParent.add_experiment()` to
        create a new Experiment object. DO NOT USE.

    .. method:: update_metadata(self, key: str, value: any) -> None:

        Update the experiment metadata using a new key value pair.

        :param key: The key of the metadata
        :type key: str
        :param value: The value of the metadata. Can be any datatype supported by JSON.
        :type value: any
        :returns: None


    .. method:: read_metadata(self) -> dict:

        Reads experiment metadata

        :returns: The experiment's metadata dictionary
        :rtype: dict

    .. method:: add_dataset(self, name: str, data_to_add: np.ndarray, datatype: any,partition:bool,trace_per_partition:int) -> 'Dataset':

        Adds a new Dataset to a given Experiment

        :param name: The desired name of the new dataset
        :type name: str
        :param data_to_add: The NumPy array of data to be added to the new dataset
        :type data_to_add: np.ndarray
        :param datatype: The datatype of the dataset
        :type datatype: any
        :param partition: Flag indicating whether to partition the dataset
        :type partition: bool
        :param trace_per_partition: Number of traces per partition
        :type trace_per_partition: int
        :returns: The newly created Dataset object
        :rtype: Dataset

    .. method:: get_dataset(self, dataset_name: str, partition:bool = False, index:int = -1) -> 'Dataset':

        Get a dataset from a given experiment.

        :param dataset_name: The name of the requested dataset
        :type dataset_name: str
        :param partition: Flag indicating whether to retrieve a partitioned dataset
        :type partition: bool
        :param index: The index of the specific partition to retrieve
        :type index: int
        :raises ValueError: If a specified partition does not exist.
        :returns: The requested dataset. None if it is not found.
        :rtype: Dataset. None if not found.
        

    .. method:: get_partition_dataset(self, dataset_name: str, partition: bool = True, index_range: tuple = (None, None)) -> np.ndarray:

        Get a dataset from a given experiment, with a start and end index passed as a range tuple.

        :param dataset_name: The name of the requested dataset
        :type dataset_name: str
        :param partition: Flag indicating whether to retrieve a partitioned dataset
        :type partition: bool
        :param range_tuple: A tuple (start_index, end_index) specifying the range for concatenating partitions
        :type range_tuple: tuple
        :raises ValueError: If a specified partition does not exist.
        :returns: The requested dataset. None if it is not found.
        :rtype: np.ndarray. None if not found.




    .. method::get_partition_dataset(self, dataset_name: str, partition: bool = True, index_range: tuple = (None, None)) -> np.ndarray:

        Get a dataset from a given experiment, with a start and end index passed as a range tuple.

        :param dataset_name: The name of the requested dataset
        :type dataset_name: str
        :param partition: Flag indicating whether to retrieve a partitioned dataset
        :type partition: bool
        :param range_tuple: A tuple (start_index, end_index) specifying the range for concatenating partitions
        :type range_tuple: tuple
        :raises ValueError: If a specified partition does not exist.
        :returns: The requested dataset. None if it is not found.
        :rtype: np.ndarray. None if not found.


    .. method:: delete_dataset(self, dataset_name: str) -> None:


        Deletes a dataset and all its contents. Confirmation required. 

        :param dataset_name: The name of the dataset to delete.
        :type dataset_name: str
        :param partition: If True, deletes a specific partition or a range of partitions.
        :type partition: bool
        :param index: The index of the specific partition to delete (if deleting a single partition).
        :type index: int, optional
        :param index_range: A tuple (start_index, end_index) specifying the range of partitions to delete.
        :type index_range: tuple, optional
        :returns: None

    .. method:: query_datasets_with_metadata(self, key: str, value: any, regex: bool = False) -> list['Dataset']:

        Query all datasets in the Experiment object based on exact metadata key-value pair or using regular expressions.

        :param key: The key to be queried
        :type key: str
        :param value: The value to be queried. Supply a regular expression if the `regex` parameter is set to true. Supplying
                        a value of "*" will return all experiments with the `key` specified in the key parameter.
        :type value: any
        :returns: A list of queried datasets
        :rtype: list['Dataset']

    .. method:: get_visualization_path(self) -> str:

        Get the path to the visualization directory for the Experiment object.

        :returns: The visualization path of the experiment
        :rtype: str

    .. method:: calculate_snr(self, traces_dataset: str,intermediate_fcn: Callable, *args: any,  visualize: bool = False, save_data: bool = False, save_graph: bool = False, partition:bool = False, index:int = None, index_range: tuple = (None, None)) -> np.ndarray:
        
        Integrated signal-to-noise ratio metric.
        
        :param traces_dataset: The name of the dataset containing trace data.
        :type traces_dataset: str
        :param intermediate_fcn: A function to compute intermediate values used for SNR calculation.
        :type intermediate_fcn: Callable
        :param *args: Additional datasets required for intermediate function parameters.
        :type *args: any
        :param visualize: Whether to generate a visualization of the SNR results.
        :type visualize: bool
        :param save_data: Whether to store the computed SNR metric as a dataset.
        :type save_data: bool
        :param save_graph: Whether to save the visualization to the experiments folder.
        :type save_graph: bool
        :param partition: Whether to compute SNR on a specific partition of the dataset.
        :type partition: bool
        :param index: Index of the partition to use if applicable.
        :type index: int
        :param index_range: The start and end indices for dataset partitioning.
        :type index_range: tuple
        :returns: The computed SNR metric as a NumPy array.
        :rtype: np.ndarray


    .. method:: calculate_t_test(self, fixed_dataset: str, random_dataset: str, visualize: bool = False, save_data: bool = False, save_graph: bool = False, partition:bool = False, index:int = None, index_range: tuple = (None, None)) -> (np.ndarray, np.ndarray):

        Integrated t-test metric.

        :param fixed_dataset: The dataset containing fixed traces.
        :type fixed_dataset: str
        :param random_dataset: The dataset containing random traces.
        :type random_dataset: str
        :param visualize: Whether to generate a visualization of the t-test results.
        :type visualize: bool
        :param save_data: Whether to store the computed t-test results as datasets.
        :type save_data: bool
        :param save_graph: Whether to save the visualization to the experiments folder.
        :type save_graph: bool
        :param partition: Whether to compute t-test on a specific partition of the dataset.
        :type partition: bool
        :param index: Index of the partition to use if applicable.
        :type index: int
        :param index_range: The start and end indices for dataset partitioning.
        :type index_range: tuple
        :returns: The computed t-test values and maximum t-values as NumPy arrays.
        :rtype: (np.ndarray, np.ndarray)

    .. method:: calculate_correlation(self, predicted_dataset_name: any, observed_dataset_name: str, order:int, window_size_fma: int, intermediate_fcn: Callable, *args: any, visualize: bool = False, save_data: bool = False, save_graph: bool = False, partition:bool = False, index:int = None, index_range: tuple = (None, None)) -> np.ndarray:

        Integrated correlation metric.

        :param predicted_dataset_name: The name of the dataset containing predicted leakage values.
        :type predicted_dataset_name: str
        :param observed_dataset_name: The name of the dataset containing observed leakage values.
        :type observed_dataset_name: str
        :param order: The order of the correlation analysis.
        :type order: int
        :param window_size_fma: The window size for filtering moving averages.
        :type window_size_fma: int
        :param intermediate_fcn: A function to compute intermediate values used for correlation analysis.
        :type intermediate_fcn: Callable
        :param *args: Additional datasets required for intermediate function parameters.
        :type *args: any
        :param visualize: Whether to generate a visualization of the correlation results.
        :type visualize: bool
        :param save_data: Whether to store the computed correlation metric as a dataset.
        :type save_data: bool
        :param save_graph: Whether to save the visualization to the experiments folder.
        :type save_graph: bool
        :param partition: Whether to compute correlation on a specific partition of the dataset.
        :type partition: bool
        :param index: Index of the partition to use if applicable.
        :type index: int
        :param index_range: The start and end indices for dataset partitioning.
        :type index_range: tuple
        :returns: The computed correlation metric as a NumPy array.
        :rtype: np.ndarray



.. class:: Dataset

    .. method:: __init__(self, name: str, path: str, file_format_parent: FileParent, experiment_parent: Experiment, index: int, existing: bool = False, dataset: dict = None):

        Creates an Dataset object. Do not call this constructor. Please use `Experiment.add_dataset()` to
        create a new Dataset object. DO NOT USE.

    .. method:: read_data(self, start: int, end: int) -> np.ndarray:

        Read data from the dataset a specific start and end index.

        :param start: the start index of the data
        :type start: int
        :param end: the end index of the data
        :type end: int
        :returns: An NumPy array containing the requested data over the specified interval
        :rtype: np.ndarray

    .. method:: read_all(self) -> np.ndarray:

        Read all data from the dataset

        :returns: All data contained in the dataset
        :rtype: np.ndarray

    .. method:: add_data(self, data_to_add: np.ndarray, datatype: any) -> None:

        Add data to an existing dataset

        :param data_to_add: The data to be added to the dataset as a NumPy array
        :type data_to_add: np.ndarray
        :param datatype: The datatype of the data being added
        :type datatype: any
        :returns: None

    .. method:: update_metadata(self, key: str, value: any) -> None:

        Update the dataset metadata using a new key value pair.

        :param key: The key of the metadata
        :type key: str
        :param value: The value of the metadata. Can be any datatype supported by JSON.
        :type value: any
        :returns: None




