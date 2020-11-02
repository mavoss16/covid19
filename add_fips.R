library(readr)
library(dplyr)
library(magrittr)

ia_counties = read_rds("county_fips.rds")

county_data = read_csv("County_data.csv")

counties_fips = left_join(county_data, ia_counties %>% select(County, co_fips))

write_csv(counties_fips, "County_data_fips.csv")

