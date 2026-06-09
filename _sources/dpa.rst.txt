Differential Power Analysis (DPA)
================================

.. method:: calculate_dpa(traces, iv, order=1, window_size_fma=5, num_of_traces=0, visualize: bool = False, visualization_path: any = None):

    Unified differential power analysis method that has support for first and second order DPA.

    :param traces: The set of power traces used for analysis.
    :param iv: Intermediate algorithm values associated with the power traces
    :param order: The order of DPA analysis (default: 1).
    :param window_size_fma: The window size used for filtering or moving average computations.
    :param num_of_traces: The number of traces to include in the analysis
    :param visualize: Whether to generate a visualization of the analysis results.
    :param visualization_path: Path to save the visualization output, if applicable.
    :return: The result of the DPA computation.

.. method:: calculate_second_order_dpa_mem_efficient(traces, IV, window_width):

    Efficient implementation of second order DPA

    :param traces: The power traces to be processed.
    :param IV: Intermediate algorithm values associated with the power traces
    :param window_width: The window size of the moving average calculation
    :returns: The result of the DPA calculation