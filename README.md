# Profiling Office Law Firms

This is a Python application that allows you to profile office law firms based on an uploaded Excel file. It applies a series of transformations to the input data and generates a profile for each row in the DataFrame.

## Installation

1. Clone the repository:

    ```shell
    git clone https://github.com/caetanyyy/advbox-profiling.git
    ```

2. Install the required dependencies:

    ```shell
    pip install -r requirements.txt
    ```

## Usage

1. Run the `app.py` file:

    ```shell
    python app.py
    ```

2. Access the application in your web browser at `http://localhost:8501`.

3. Upload an Excel file containing the data you want to profile. The file should be in the `.xlsx` format.

4. Select the sheet and columns that correspond to the number of lawsuits, number of collaborators, and 12-month revenue.

5. Click the "Profile Table" button to apply the transformations and generate the profiled table.

6. The profiled table will be displayed on the screen. You can also download it as an Excel file by clicking the "Download Profiled Table" button.