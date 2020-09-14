## Question

### Given an input matrix as a CSV file with NAN values, write a command-line script that will generate an output matrix as a CSV file where the NAN values are interpolated as the average of the neighboring non-diagonal values.

### The values of the non-NAN values should be preserved in the output matirx.

## Answer

Python version 3.8.2

modules:

* os
* sys
* argparse
* logging
* csv
* numpy

### Usage

* Help:

`python interpolator.py --help`


* Production mode:

`python interpolator.py -i input_csv_path -o outout_csv_path`
