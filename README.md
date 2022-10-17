# CECP-decision-making-tool

### Authors
Croci Francesco\
d’Arenzo Daniele\
Fumagalli Alberto\
Gambaro Enrico\
Neri Francesco\
Samandari Ahmad

## Libraries to install:
- progress
- sklearn
- dash-extensions  *  (name is correct, avaible through pip3)
- google  
- matplotlib
- requests  *
- scipy
- seaborn

## EXECUTE DASHBOARD
Dash is developed for an "offline mode", so data is instantly avaible but is possible to set constant updates that will download new data in a time interval provided.
To execute dashboard, install all module provided by "*" marker and ONLY execute file "index.py". (dashboard is tested on chromium platforms)


## STEPS TO RETRIEVE PUBMED PAPERS USING A TRAINED ESTIMATOR:
1) go to Script_alone\PubMed_classification
2) open main.py and modify the search query
3) open validation.py and modify X_train/Y_Train using manually classified papers
4) open Dict.txt and put all the keywords for your dictionary, *THIS IS NOT THE FINAL DICTIONARY*, classificator will choose a combination of them which maximize the training score.
6) if you want to find a better Estimator, edit threshold in line 76 of Validation file (condition to exit loop and retrieve best parameters+current sub-dictionary) 
5) pertinent papers will be added to a csv file at the end of the process
x) warning!! be sure no desktop.ini file in dictionaries folder otherwise code will fail


## STEP TO APPEND DEV_TYPE/MED_FIELD TO AN EXISTING CSV FILE:
1) go to Script_alone\Find_device_type    OR  Script_alone\Find_medical_Field
2) if you don't have devices.csv file (csv containing only devices name column) execute main.py in the folder extract_device_column
3) to provide flexibility, we added min-max value of search (to split work in different stages, becouse it requires a lot of time) in the file main.py
4) Execute main.py, a file is added in the folder during the process containing values found
5) After getting all the ranges, put all the files in merging\range folder and run Merge_ranges.py, be sure you have in the merging folder result.csv file (df to attach new column)
x) warning!! be sure no desktop.ini file in dictionaries folder otherwise code will fail


## FAQ
-What is the content of Script_alone folder?
	here there are files and scripts independent from the execution of dashboard, used to retrieve data during developing or to test features.
-why init file in pages folder?
	becouse the folder become a package for python and all the variables inside file "init" are treated as global variables
-what is the content of asset folder?
	it contains necessaries CSS files to customize GUI and prevent some bug
-what is the content of data/papers folder?
	it has all the csv files with all device type names, containing all papers related to specific device type  (we have only insulin pump becouse of project design features, otherwise they would be there files like "pacemaker.csv", "scalpel.csv" etc)
