# Vizdom
Link to hosted server (Needs NTNU VPN to access): http://10.24.92.68:8080/  
Link to user-manual: https://github.com/Pipe-Runner-Lab/vizdom/wiki/User-Manual
Link to Github repo: https://github.com/Pipe-Runner-Lab/vizdom

![image](https://user-images.githubusercontent.com/19551058/208308797-727b84ad-7945-4da0-bcbb-28af61f9299e.png)
![image](https://user-images.githubusercontent.com/19551058/208308836-4049d26c-bda1-4434-b38c-5f7881d1b9ce.png)
![image](https://user-images.githubusercontent.com/19551058/208308853-bd2a7dc1-9798-4ff9-ab30-92c608da7da4.png)

## Setup
In some cases, above steps might not work. You can following the given steps below:  
`conda create -n vizdom python=3.9`  
`conda activate vizdom`  
`conda install pandas numpy scikit-learn`  
`pip3 install singleton_decorator dash dash_bootstrap_components`

# Running Data Pipeline
We have a sophisticated data pipeline which runs using cron job every 24 hours on the server. For running the project locally, you need to run the pipeline since it populates the data in the database. The use of database in our project is crucial to deliver a smooth user experience. When running locally, you'll have to configure the cron job yourself. Since we already do it on the server, you can use our hosted app instead.  

When in the project root:  
`cd src`  
`python pipeline.py`

# Starting the Server
When in the project root:   
`cd src`  
`python app.py` 
   
This will start a local server in dev mode.
