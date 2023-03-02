## Using this Scraper 

1. Clone this repository
2. In the `scraper` directory, run `yarn install`
3. Go to https://directory.columbia.edu/people/browse/students, log in, and click `A` from the alphabet selection bar.  
4. Copy `.env.example` to `.env` and add in your own cookie.
5. Run `yarn main` to scrape every page of the directory and save it into `data2.json`. Feel free to change the datafile name.