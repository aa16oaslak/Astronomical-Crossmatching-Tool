# Please go through this readme file before accessing the contents of this repository.
This readme file contains details regarding the GUI Tool for cross-matching two astronomical catalogues. First, ensure that both catalogs are in csv format and you know all the details regarding the columns/attributes of both catalogs. Now you can follow the below steps to get your cross-matched master catalog.

Steps to use the cross-matching tool:
- Open and Run the cross_matching_tool.py file from the repository in a python interpreter (Ensure that Tkinter, NumPy, pandas, astropy libraries are already installed in your interpreter).
- After executing the code successfully, a new window should appear in your console. There enter the file directories of the catalogs that you want to cross-match in the correct format. Please ensure that your catalogs are in csv format. After that, click Next.
- Then a second window will pop up on the screen. Enter the column number where right ascension and declination are present in both the catalogs. After that, enter the required details in the entry boxes.
- After filling in all the entries, click the button on the bottom of the window. You can now check your master catalog in the local file directory.  
