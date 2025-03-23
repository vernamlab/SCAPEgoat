# SCAPEgoat

SCAPEgoat addresses issues in existing toolkits used in the entire SCA chain through simple file structures, support for standard capture hardware, and a post-processing software suite. The idea behind the design of SCAPEgoat (SCA with high Performance Evaluation + WPI's mascot that is a goat) is to create modules corresponding to (virtually all) steps taken in SCA. The modular nature of SCAPEgoat enables the user to enjoy each module separately or as a complete framework. 
Moreover, SCAPEgoat introduces memory efficiency, especially regarding RAM usage for large datasets, making our tool ideal for newcomers. 

Paper: https://eprint.iacr.org/2025/499.pdf
Documentation: https://vernamlab.org/SCApeGoat

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Capturing](#capturing)
  - [Post-Processing](#post-processing)
- [License](#license)
- [Contact](#contact)

## Features

- Modular framework for SCA, enabling users to work with individual components or the entire suite.
- Improved memory efficiency, allowing for the handling of large datasets.
- Computation of various SCA metrics such as Signal-to-Noise Ratio (SNR), Test Vector Leakage Assessment (TVLA), Correlation Power Analysis (CPA), and t-tests.
- Support for partitioned data analysis based on single index values or index ranges.
- Streamlined integration with ChipWhisperer and other standard SCA tools.

## Installation

1. **Install ChipWhisperer**:
   - Follow the installation instructions in the [ChipWhisperer documentation](https://chipwhisperer.readthedocs.io/en/latest/).
   - *Note*: This step is only necessary to capture new traces.

2. **Clone the Required Library**:
   - Clone the cwtvla folder from the [ChipWhisperer-TVLA repository](https://github.com/newaetech/chipwhisperer-tvla) into the ChipWhisperer directory.
   - Set the appropriate path for the imports in the Jupyter Notebook.

3. **Download Traces**:
   - You can obtain traces from one of the following sources:

     **i. EM for Good Repository**:<br/>
     Download the required traces from the provided link [EMSCA Traces](https://app.box.com/v/EMSCA-for-good). The dataset can be partially downloaded, but you must maintain the folder structure:
     - (CEMA->Experiments/metadata.json->(downloaded the need experiment)->(partially download the datasets too)).
    
     **ii. Bake It Till You Make It Repository**:<br/>
     Download the required traces from the provided link [BITUMI Traces](https://app.box.com/v/BITUMI-traces). The dataset can be partially downloaded, but you must maintain the folder structure:
     - (BITUMI_scape->Experiments/metadata.json->(downloaded the need experiment)->(partially download the datasets too)).
   

4. **Organize Notebooks and Traces**:
   - Place the main Jupyter Notebook within the appropriate directory, ensuring it is correctly positioned relative to any required folders or dependencies.
   - Verify that any supporting notebooks or scripts are located in the correct directory or update file paths accordingly.
5. **Verify Import Paths**:
   - Ensure all import paths are correctly set in relevant notebooks or scripts to prevent execution errors.

## Usage

SCAPEgoat supports both trace capturing and post-processing.

### Capturing

Capturing requires the following equipment:

- CW Husky/Lite capture board
- CW Lite target board
- EM probe (compatible with SMA connections to the CW capture board)
- XYZ stage (Riscure/Keysight)

Each of these components has associated Python libraries for control. The SCAPEgoat library is utilized for file management and scope configuration during capture for storage and management.

**Steps**:

1. **Initialization**:
   - Use `Setup_script` to compile the necessary C code.
   - Set up the scope and target using the `scope` class from the SCAPEgoat library.

2. **Experiment Management**:
   - Initialize a parent directory to store experiments.
   - Create a new experiment and initialize capture using the grid tracing function.

3. **Data Collection**:
   - Capture fixed and random traces for each grid location.
   - Store the captured data as datasets within the experiment.

### Post-Processing

SCAPEgoat provides built-in functions for various post-processing tasks, including metric computation.

**Metric Computation**:

SCAPEgoat supports multiple SCA metric calculations, including:

- Signal-to-Noise Ratio (SNR): Evaluates the the ratio of signal power to the noise power.
  
```
exp.calculate_snr("random_trace", compute_bitwise_operations, 100, x0, x1, x3, x4, -1, "y4", partition=True, index=2, visualize=True)
exp.calculate_snr("random_trace", compute_bitwise_operations, num_traces, x0, x1, x3, x4, -1, "y4", visualize=True, partition=True, index_range=(0, 9))
```

- Test Vector Leakage Assessment (TVLA): Identifies significant variations in leakage across different trace sets.

```
exp.calculate_t_test("fixed_trace", "random_trace", partition=True, index=3, visualize=True)
exp.calculate_t_test("fixed_trace", "random_trace", partition=True, index_range=(0, 9), visualize=True)
```

- Correlation Power Analysis (CPA): Measures correlation between predicted and actual power consumption.

```
a, b, c = exp.calculate_correlation("leakage", "random_trace", 1, 5, compute_hw, x0, x3, x4, target_byte, visualize=True, partition=True, index_range=(0, 9))
a, b, c = exp.calculate_correlation("leakage", "random_trace", 1, 5, compute_hw, x0, x3, x4, target_byte, visualize=True, partition=True, index=0)
```

## License

This project is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

## Contact

If you have any questions or want to report a bug, please email me at [dmmehta2@wpi.edu](mailto:dmmehta2@wpi.edu).



# Available github projects using SCAPEgoat

[Bake it till you make it](https://github.com/vernamlab/Bake-it-till-you-make-it) - This is a dataset where a binary neural network is put under stress by increasing the temperature. Details can be found in the paper [Bake it till you make it: Heat-induced Power Leakage from Masked Neural Networks](https://ojs.ub.ruhr-uni-bochum.de/index.php/TCHES/article/view/11803)

[EM for good](https://github.com/vernamlab/EM-for-good) - This is a dataset for the EM traces collected from unmasked AES implementation on CW-lite. 
