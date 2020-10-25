# covid19
Repository containing Iowa statewide and county data on Covid-19 and R code for analysis

### Data Notes
Updated county-level data is downloaded daily from coronavirus.iowa.gov, beginning on June 21, 2020. <br>
Calculations use current total positive tests and total tests by county, subtracting the previous day's totals to find the amount for the current day. <br>
Rolling positive test rates are calculated using positive tests and total tests from the previous 14 days, with up to a day's leeway in either direction due to several instances of forgetting to download data until the next morning. <br>
The rolling positive test rate for the first two weeks includes fewer than 14 days' data. <br>
Data was not collected from 8/10-8/15 due to the August 10 wind storm. As a result, the rolling positive test rate for 8/16-8/29 is actually a 21 day positive test rate.

I have consistently calculated positive test rates that are much higher than those seen on coronavirus.iowa.gov. My data is more similar to that on iowacovid19tracker.org. The publicly available county-level data is not sufficient to replicate the positive test rates on coronavirus.iowa.gov. The site does not have any information about how the data is collected, published, or calculated, so it is difficult to explain the large disparity. 