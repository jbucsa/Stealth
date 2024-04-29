# Stealth

## Terminal Commands

### Creating the VENV environment

```bash
py -m venv venv
```

    
### Activating the VENV environment

- For Command Prompt - cmd
    
```bash

C:\Users\User\Stealth> venv\Scripts\activate.bat

(venv) C:\Users\User\Stealth> 

```
   
- For Git Bash - bash
    
```bash
User@User MINGW64 ~/Stealth (main)
$ source venv/Scripts/activate

(venv) 
User@User MINGW64 ~/Stealth (main)
$ 

``` 

### Deactivating the VENV environment


- For Command Prompt - cmd

```bash
(venv) C:\Users\User\Stealth> venv\Scripts\deactivate.bat

C:\Users\User\Stealth> 

```
   
- For Git Bash - bash
    
```bash
(venv) 
User@User MINGW64 ~/Stealth (main)
$ deactivate

User@User MINGW64 ~/Stealth (main)
$ 

``` 


## PIP Installs

What was actually installed

### Task No.1

```bash
pip install pandas
pip install plotly
pip install nbformat
```

### Task No.2
```bash
pip install pandas
pip install yfinance
pip install matplotlib
pip install seaborn 
```


## Task No.1
### Description 
A text file named data.txt is attached to this message.
Within that text file is a list of points representing the "dollar value" of a mystery stock at a certain time. 
The values are from the past 1 year of that stock.
For example, the first point in the text file is:
```1679544000000,158.93```
```1679544000000``` represents the number of milliseconds that have past since the date January 1st 1970,
```158.93``` represents the dollar value of the stock at that time.

What I would like you to do is, create a program that generates a graph of all the points.

Bonus Challenge: Create a program that finds other stocks that have "similar" graphs to the stock in the text file, and figure out what the mystery stock is.

Recommended Tools: Python, Matplotlib, Jupyter Notebook

### Solution

![Create Post](/READMD_Asset/TaskNo1/TaskNo1.png)

## Task No.2

### Description 

#### Step 1
Choose any one of the ten companies below:
```bash
Vertiv
Cameco
First Solar
Caterpillar Inc
Franklin Resources Inc
Energy Transfer LP
Cisco Systems Inc
Comcast Corp
Li Auto
BWX Technologies
```

Company choose:
```bash
Franklin Resources Inc
```

#### Step 2
Then, create an investigative report on the company you have chosen.
Include the following information at minimum:
```bash
-Visual-based analysis of past two years of market data in one month ticks: include trading volume, earnings, and share price at minimum
-Three significant events that have occurred with the company in the past year
-The dominant shareholders of the company
-The goal / philosophy of the company
-A holistic analysis of whether the company is a good investment
```


### Solution
[Link to Full Stock Report for Task No. 2](/reports/TaskNo2/Bucsa_Justin_Franklin_Resources_Report.pdf)
!["Task No 2 Solution Page 1"](/READMD_Asset/TaskNo2/ReportPage1.jpg)
!["Task No 2 Solution Page 2"](/READMD_Asset/TaskNo2/ReportPage2.jpg)
<!-- [Task No 2 Solution Page 3](/READMD_Asset/TaskNo2/ReportPage3.pdf) -->