This project contains various python scripts and shell scripts used to scrape 
various course sites and place them in an organized file system for easy, 
public access.

Overall Execution Process
- Python web scrapers are executed in background processes that continue to run
    when the user exits their terminal
- All the scraped files are put in a specified directory, namely an apache 
    hosted directory so that it can be seen from my site
- These scraping procedures are run at intervals and so modifications to the 
    files either on this server or where they are being scraped from will be
    carried over into the web-accessible files, thus keeping them up to date

Python Scraping
- each course's file scraping associated with exactly one python script
- python scripts loop indefinitely as to scrape consistently at given intervals
- places files in a specified file system, i.e. a public apache shared folder

Shell Scripts
- runScraper.sh simply executes a single python script
    - this will be either duplicated later (one for each script) or removed so that
        the next shell scripts can simply make the python calls
- runBackgroundScraper.sh - executes the runScraper.sh file(s) each with a 
    nohup call. Running each as a background process and saving the pid in a file 
    for later termination
- killBackgroundScraper.sh - uses the save_pid.txt file created by the previous 
    script to kill all scraper processes.