# 1. Implement a simple ATM controller

## 1.1. Environment
- Windows 10

## 1.2. Prerequisites
Please first install the following prerequisites in the computer:
- Python 3.9.10
- Virtualenv 20.13.1

### 1.2.1. Install Python 3.9.10
- Download the python installer "Windows installer (64-bit)" in [link](https://www.python.org/downloads/release/python-3910/)
- Install python by following the instructions in the installer
- After install python, add the following paths to environment variable "Path":
  - `%USERPROFILE%\AppData\Local\Programs\Python\Python39`
  - `%USERPROFILE%\AppData\Local\Programs\Python\Python39\Scripts`

### 1.2.2. Install Virtualenv 20.13.1
- Run the following command in cmd:
```
pip install virtualenv==20.13.1
```

## 1.3. Setup
- Create a folder called "SampleATMController"
- cd to the folder "SampleATMController" in cmd
- Run the following command in cmd

```cmd
git clone https://github.com/ivanyu199012/SampleATMController.git

virtualenv bearEnv
bearEnv\Scripts\activate

cd SampleATMController
pip install -r requirements.txt
```

## 1.4. Test
- Run the below command in cmd
```cmd
python atm_controller_test.py
```
