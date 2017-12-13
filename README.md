# chinaventure.cn-spider
By Selenium webdriver, crawl the infomation about investing activities listed on https://www.chinaventure.com.cn/event/list.shtml <br />

All infomation in the highlighted box are crawled, for all the events available. <br />
[Information to be crawled](pics/input.png) <br />

The output is saved into a single .csv file. <br />
[The output looks like this](pics/output.png) <br />
The extra columns and redundant column names are generated during batch processing and can be easily removed afterwards. <br />

Running environment: <br />
python-2.7.12, ubuntu-16.04-LTS, latest Firefox (with geckodriver executable) <br />

Configure: <br />
Please first execute config.sh to ensure all packages required are installed. 
