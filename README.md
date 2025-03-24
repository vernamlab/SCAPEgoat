# **SCAPEgoat**  

SCAPEgoat is a modular framework for side-channel analysis (SCA) that simplifies the entire SCA workflow, from trace acquisition to post-processing. It addresses limitations in existing toolkits by offering:  

- **Efficient file structures** for better trace organization.  
- **Support for standard capture hardware** such as ChipWhisperer.  
- **Optimized memory usage**, making it ideal for handling large datasets.  
- **Modular design**, allowing users to utilize individual components or the full framework.  

The name **SCAPEgoat** originates from **SCA with high Performance Evaluation** and is inspired by WPI’s goat mascot.  

📄 **Paper**: [ePrint 2025/499](https://eprint.iacr.org/2025/499.pdf)  
📖 **Documentation**: [SCAPEgoat Docs](https://vernamlab.org/SCAPEgoat)  


## **Features**  

SCAPEgoat provides a robust and modular approach to side-channel analysis with the following key features:  

- 🔹 **Modular Framework** – Use individual components or the entire suite based on your needs.  
- 🚀 **Optimized Memory Usage** – Designed to efficiently handle large datasets, reducing RAM overhead.  
- 📊 **Comprehensive SCA Metrics** – Compute key SCA metrics, including:  
  - Signal-to-Noise Ratio (SNR)  
  - Test Vector Leakage Assessment (TVLA)  
  - Correlation Power Analysis (CPA)  
  - t-tests for leakage detection  
- 📂 **Partitioned Data Analysis** – Perform trace analysis based on specific indices or index ranges.  
- 🔗 **Seamless Hardware Integration** – Supports ChipWhisperer and other standard SCA tools for trace collection.  


## **Installation**  

Follow these steps to set up SCAPEgoat:  

### **1. Install ChipWhisperer (Recommended for Smooth Experience)**  
- While ChipWhisperer is optional if you're only performing post-processing, installing it is recommended for a seamless experience.  
- Follow the official [ChipWhisperer installation guide](https://chipwhisperer.readthedocs.io/en/latest/).  

### **2. Clone the SCAPEgoat Library**  
- Clone the SCAPEgoat repository to your system:  
  ```bash
  git clone https://github.com/vernamlab/SCAPEgoat.git
- This contains all the necessary modules for trace handling and post-processing.

### **3. Clone and Set Up `cwtvla` for Leakage Detection Metrics**  
- SCAPEgoat relies on `cwtvla` for certain statistical leakage tests. Clone the `chipwhisperer-tvla` repository:  
    ```bash
    git clone https://github.com/newaetech/chipwhisperer-tvla.git
- Move the cwtvla folder into the WPI_SCA_LIBRARY folder inside the SCAPEgoat library.

### **4. Ensure Proper Import Paths**  
Add the SCAPEgoat library to your system path to ensure smooth usability:  
    ```python
    import sys
    sys.path.append("/path/to/SCAPEgoat")
This allows scripts and notebooks to access SCAPEgoat modules without manual path modifications.

## **Usage**

SCAPEgoat allows users to manage experiments efficiently and perform post-processing to compute various metrics.

1. **Initialize Project:**
   - Begin by setting up the parent directory for your project. This will be the main directory where all experiments and associated datasets are stored. For each experiment, create a dedicated subdirectory to help organize your files effectively.

2. **Dataset Management:**
   - For each experiment, datasets can be added in two ways:
     - **Using existing data:** You can upload previously captured datasets directly into the experiment.
     - **Capturing new data:** If you need new data, you can use supported devices for capturing traces. Supported devices include:
       - **CW devices** such as scopes and target boards
       - **LeCroy scopes** via the pyVISA interface
     - SCAPEgoat allows you to manage data for each experiment flexibly, whether it’s from previously collected data or fresh traces.

3. **Post-Processing:**
   - Once datasets are available, you can proceed to post-processing, where you compute the desired metrics based on the experiment's needs. SCAPEgoat supports various metrics such as Signal-to-Noise Ratio (SNR), Test Vector Leakage Assessment (TVLA), and Correlation Power Analysis (CPA), among others.


For actual code examples and further guidance, please refer to the **demo** folder in the SCAPEgoat repository. It contains sample code that demonstrates how to set up experiments, manage datasets, and perform post-processing.

You can also explore datasets from the following sources for example usage:
     - **EM for Good**: A dataset for the EM traces collected from unmasked AES implementation on CW-lite. You can find it in the [EM for Good GitHub repository](https://github.com/vernamlab/EM-for-good).
     - **Bake it Till You Make It**: A dataset where a binary neural network is put under stress by increasing temperature. You can find it in the [Bake it Till You Make It GitHub repository](https://github.com/vernamlab/Bake-it-till-you-make-it).

## **References**

1. **SCAPEgoat:**
   - Mehta, D., Ganji, F. (2025). SCAPEgoat: A Modular Framework for Side-Channel Analysis with Enhanced Memory Efficiency. Available at: [https://eprint.iacr.org/2025/499.pdf](https://eprint.iacr.org/2025/499.pdf).

2. **Bake it Till You Make It:**
   - Mehta, D., Ganji, F., et al. (2025). "Bake it Till You Make It: Heat-Induced Power Leakage from Masked Neural Networks." In *TCHES*. Available at: [https://ojs.ub.ruhr-uni-bochum.de/index.php/TCHES/article/view/11803](https://ojs.ub.ruhr-uni-bochum.de/index.php/TCHES/article/view/11803).

3. **EM for Good:**
   - Mehta, D., Ganji, F., et al. (2025). "EM for Good: A Dataset for Electromagnetic Trace Collection of Unmasked AES Implementations." Available at: [https://github.com/vernamlab/EM-for-good](https://github.com/vernamlab/EM-for-good).


## License

This project is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

## Contact

If you have any questions or want to report a bug, please email me at [dmmehta2@wpi.edu](mailto:dmmehta2@wpi.edu).
