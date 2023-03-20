import axios from 'axios';
import { parse } from 'node-html-parser';
import * as he from 'he';
import * as fs from 'fs/promises';
import * as dotenv from 'dotenv';
dotenv.config();

const sleep = ms => new Promise(r => setTimeout(r, ms));

// Parses columbia directory to fetch all items.
// Note that you may have to fetch the cookies from your browser and update the cookie header from the .env file.

async function getDirectoryHTML(initialLetter: string = 'A', pageNumber: number = 1) {
  const res = await axios.get(
    `https://directory.columbia.edu/people/browse/students?filter.initialLetter=${initialLetter}&page=${pageNumber}`,
    {
      headers: {
        accept:
          'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not A(Brand";v="24", "Chromium";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        cookie:
          process.env.COOKIE,
        Referer: 'https://cas.columbia.edu/',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
      },
    },
  );
  return res;
}

async function main() {
  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  const allItems: any = [];

  for (const letter of alphabet) {
    console.log('Fetching letter: ', letter);
    let pageNumber = 0;

    while (true) {
      console.log('Fetching page: ', pageNumber);
      const html = await getDirectoryHTML(letter, pageNumber);
      const root = parse(html.data);
      const items = root.querySelectorAll('body > div > form > table > tr:nth-child(5) > td:nth-child(2) > div > table > tr').slice(1);
    
      const parsedItems = items.map((item) => {
        const name = item.querySelector('a')?.innerText;
        const role = item.querySelector('td:nth-child(2)')?.innerHTML;
        const address = item.querySelector('td:nth-child(3)')?.innerText;
        const email = item.querySelector('td:nth-child(4) > a')?.innerText;
    
        const data = {
          name,
          role,
          address: address ? he.decode(address) : null,
          email: email ? he.decode(email) : null,
        };
        return data; 
      });

      if (pageNumber > 0 && parsedItems[parsedItems.length - 1].name === allItems[allItems.length - 1].name) {
        break;
      }
  
      allItems.push(...parsedItems);

      
      pageNumber++;
    }

    await sleep(1000);
    
  }

  
  await fs.writeFile('data2.json', JSON.stringify(allItems, null, 2));

}

main();
