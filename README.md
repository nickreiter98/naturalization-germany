# Welcome to my Data Visualisation Project: Naturalization to Germany

## 🌟 Thank you for visiting my GitHub repository!
In this project, my goal is to discover insights and patterns within complex datasets. By converting raw data into clear visual stories, I strive to make information easily accessible and understandable to all.

<br>

## 💼 Use Case

Germany is facing a big lack in skilled workers. In order to overcame this challenge, enterprises have to address possible employees, who found their new home in Germany. Eminent advantage hereby is gained by insights into the composition of naturalized persons and the cultural preferences through language, customs or religion. This is not only supporting the HR to address better future potential employees but also to prepare the enterprise itself for enhanced multicultural work environment. 

<br>

## 📊 About the Data 
As underlying data, I use a rich dataset obtained from the Federal Statistical Office of Germany's [GENESIS](https://www-genesis.destatis.de/genesis/online) online database. Specifically, I am using the data set conataining various infomations of the naturalization to Germany. You can find this dataset [here](https://www-genesis.destatis.de/genesis//online?operation=table&code=12511-0014&bypass=true&levelindex=1&levelid=1710171917348#abreadcrumb). Literally, Genesis is a goldmine for anyone keen on understanding the intricate details and social trends of various governmental domains in Germany.

<br>


## 💪🏻 How to start

1) Create a virtual environment and install all required dependencies
    ``` Bash
    python3 -m venv .venv --prompt naturaliz-ger
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

2) The Graphics are shown in an interactiv manner. Thus, you have to start Dash. This can be done in twofold ways.
    
    - **Script:** run `python3 app.py` in the cli
    - **Docker:** navigate to the project's root and run following cli commands
        ``` Bash
        docker build -t naturalization-germany .`
        docker images
        docker run -d -p 5000:5000
        ```
<br>

## 📝 Project Overview

- Getting insides into the composition of German naturalization using graphical representatino of the underlying data
- Helping enterprises to target specific group for recruitment purposes
- Dataset contains 6601 data points collected by the German Federal Statistic Bureau
- Data is split in a multidimensional into several distinct features: *year, sex, age group, region of origin, marital status* 

<br>

## 🌟 Key Challenges

- Cleaning, manipulating and transforming data for better handling
- Chosing appropriate graphical techniques to show underlying trends
- Dockerizing the app to launch on AWS

<br> 

## 🔎 Insights

- Most naturalized persons are originating from Europe or Near East
- The distribution among men and women is pretty equal, but outliers are slighty more occuring on the female side (East Africa, Central America and Caribics)
- Persons are in average around 35 years old
- A clear trend to people coming to people alone (not married)
- Trends towards naturalization are politicaly influenced. E.g. immigration from GB climbed after the Brexit, also the naturalization from Near East has been increasing since the Arabic Spring



