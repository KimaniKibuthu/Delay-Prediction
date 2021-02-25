# Flight Delay Predictions
This project aims at creatin an application that can assist in predicting flight delays.

To assist, there are three important files:
* app.py
* catboost_model.pkl

## Deploying the application
The process is as follows:
1. Create a free tier amazon account.
2. On EC2, launch an instance.
3. Under the Amazon Machine Interface1.	Create instance.
4. Choose an Amazon Machine Image (Ubuntu Server 18.04 LTS (HVM), SSD Volume Type).
5. Choose an instance type (t2 micro).
6. Configure Security Group (Add a custom TCP port at 8501 and allowing access from anywhere)
7. Launch instance and download the access key.
8. Save the access key in a particular folder. In the folder with the downloaded access key, open a powershell.
9. Connect to the ubuntu server via ssh using the access key and your public DNS generated once you created an instance. To see how you can do this, click **connect** on the instance that you created. You will have a detailed explanation on how to go about this. 
10.	Install the necessary libraries needed. In my case streamlit, miniconda and catboost.This is as shown below.
`sudo apt-get update`

`wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh`

`bash ~/miniconda.sh -b -p ~/miniconda`

`echo "PATH=$PATH:$HOME/miniconda/bin" >> ~/.bashrc`

`source ~/.bashrc`

`pip install streamlit`
`pip install catboost`

11.	Using WinSCP, upload the web app file and the model file into the Ubuntu server.
12.	Start a tmux session to ensure the continued operation of the application even after the powershell and the ssh are closed.
`sudo apt-get install tmux` - Install tmux
`tmux new -s nameofsession` - Create session
`streamlit run app.py` - Run the app.py



