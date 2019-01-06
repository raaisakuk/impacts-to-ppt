# ImPACTS to PowerPoint

This package allows one to get a powerpoint from the results of their [ImPACTS](https://medicine.yale.edu/lab/impacts/) survey which are stored in an excel file.

## Prerequisites

This package requires Python 2.7 and is not compatible with Python 3.x.

## Installing and Running the demo

1. Clone or download the repo from github
2. Go to the downloaded directory and run the following command:

```
python setup.py install
```

3. Go to the "pedsim" directory and run the follwing command.

```
python report.py AP ../demo/demo-excel-without-error.xlsx ../demo
```

This will create a powperpoint named AP.pptx in the [demo](https://github.com/raaisakuk/impacts-to-ppt/tree/master/demo) using the data of the hospital named "AP" from [demo-excel-without-error.xlsx](https://github.com/raaisakuk/impacts-to-ppt/blob/master/demo/demo-excel-without-error.xlsx).

## Authors

* **Raaisa** 
* **Bora Raghu Ram Reddy**

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/raaisakuk/impacts-to-ppt/blob/master/LICENSE) file for details