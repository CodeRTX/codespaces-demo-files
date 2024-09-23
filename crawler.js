const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

const visitedUrls = new Set();
let results = [];

// Load existing results
if (fs.existsSync('results.json')) {
    const existingData = JSON.parse(fs.readFileSync('results.json'));
    results = existingData;
    existingData.forEach(item => visitedUrls.add(item.url));
}

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function crawl(url, depth) {
    if (depth === 0 || visitedUrls.has(url)) {
        return;
    }

    visitedUrls.add(url);

    try {
        const { data } = await axios.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        });
        const $ = cheerio.load(data);
        const links = [];

        $('a').each((index, element) => {
            const link = $(element).attr('href');
            if (link && link.startsWith('http')) {
                links.push(link);
            }
        });

        results.push({ url, links });
        console.log(`Crawled: ${url}`);

        for (const link of links) {
            await delay(1000); // Add a delay of 1 second between requests
            await crawl(link, depth - 1);
        }
    } catch (error) {
        console.error('Error fetching the page:', error);
    }
}

function saveResults() {
    fs.writeFileSync('results.json', JSON.stringify(results, null, 2));
    console.log('Results saved to results.json');
}

const startUrl = 'https://www.gktoday.in/daily-current-affairs-quiz-september-22-23-2024/';
const maxDepth = 2;

crawl(startUrl, maxDepth).then(saveResults);
