# Social Mentions Scraper

Scrapes google search by provided query and search results to check them for social networks mentions.

To run scraper execute:
`scrapy runspider spiders/social_mentions_spider.py -a file=<path_to_file_with_queries>`

Result will be provided in txt file formated as:
`key_word, first_result_url, has_twitter, has_facebook, has_instagram`

Results file name can be changed with DEFAULT_OUTPUT_NAME setting.

To automatically upload results file to AWS S3 you have to set BUCKET_NAME setting.