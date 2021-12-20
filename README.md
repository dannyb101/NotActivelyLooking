<h1>Python Webscraper</h1>

This aim of this project was to automate downloading and re-uploading CV's between two different websites that I was required to do as part of role. 

The requirement was to create client profiles for users who had recently registed with the website. These profiles could be auto-generated from CV's if the user had uploaded one or from LinkedIn if not.

I acheived the scraping using the Selenium pakage in Python. The first script (NALScrape.py) automated a browser which would click through user profiles downloading CV's, if they were present, and organising them by registration date. If no CV's were present the user name and registration date were saved to a text file for manual input at a later stage. 

The second script NALEzekia.py then automated another browser window and uploaded the CV's including user names and registration dates.

This project replaced the manual data input process reducing ingestion time by 90%
