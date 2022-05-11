# Data Collection Pipeline

This project wil be used to illustrate how to use webscraping libraries to showcase the ability to create a Python class with all the necessary methods to collect data from the website including how to browse the website, how to extract data from the website, how to save the data to a database, etc.
_______________________________________________________________________________________________________________________________________________
## Milestone 1: Setting up Conda Environment and Web Driver (Completed)
 
 - For this webscraping project, Chrome Version (Version 101.0.4951.54) was downloaded for Ubuntu and will be used as the main browser for this webscraping project.

- The corresponding [ChromeDriver](https://chromedriver.storage.googleapis.com/index.html?path=101.0.4951.41/) (Version 101.0.4951.54) was then downloaded to be used as the main driver for the project.

- Next, a conda environment was set up with the necessary dependencies including `selenium`, `pip` and `ipykernel`. 

      # Setting up conda environment:
      conda create --name Data_Collection_Pipeline
      conda activte Data_Collection_Pipeline
      
      conda install pip
      conda install selenium
      conda install ipykernel
      conda install BeautifulSoup4
     
------------------------------------------------------------------------------------------------------------------------------------------------
