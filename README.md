# Practice It Web Scraper

This scirpt will parse your PracticeIt profile and create files for all puzzles that you have attemped and completed. 

Please note that if you intended to upload your solutions to github, you are doing so against the academic policy of the University of Washington. To avoid this, you should create a private repository (you can get free private repositories using your student email). 

## Usage

To use the program, install the necessary dependencies. Then, update your login information in `config.json`. Finally, run the script using the following command: 

`python scrape.py`

The program will create a seperate file for every problem that you have attempted. Please note that practice it considers a problem attempted if you opened the file, but did not write inside of it. This will create a number of files in the `PracticeItScraper` direcotry that are empty. 

## TO-DO:

* Remove empty files
* Write files to sperate direcotry
* Write files with .java extension
* Create sub-directories for different problem types
* Write script to upload changed files to github
