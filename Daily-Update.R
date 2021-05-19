library(data.table)
library(lubridate)
library(dplyr)
# library(magrittr)
# library(stringr)

# Create File Names
today = Sys.Date()
yesterday = Sys.Date() - 1
today_file = paste("year2_", month(today), "-", day(today), ".csv", sep = "")
yesterday_file = paste("year2_", month(yesterday), "-", day(yesterday), ".csv", sep = "")


today_file = file.path("Daily-Data", today_file)
yesterday_file = file.path("Daily-Data", yesterday_file)

# Get Data
data_today = fread(today_file, col.names = c("County", "IndTested", "IndPositive", "IndRec", "Deaths", "Deaths_underly", "Deaths_contrib"))
data_today = data_today[, 1:5]
data_yesterday = fread(yesterday_file)
statewide = fread("State_data.csv")
county_data = fread("County_data.csv")


# Organize the data from today
data_today[, c("Date", "Year", "Month", "Day") := list(today, year(today), month(today), day(today))]
data_today = data_today[order(County)]
data_today = data_today[County != "Pending Investigation"]


# Update county data
data_today = data_today[, c("NewIndTested", "NewIndPositive", "NewIndRec", "NewDeaths", "PosTestRate", "ID", "PosTestRate14") := list(0, 0,0,0,0,0,0)]
data_today$NewIndTested = data_today$IndTested - data_yesterday$IndTested
data_today$NewIndRec = data_today$IndRec - data_yesterday$IndRec
data_today$NewDeaths = data_today$Deaths - data_yesterday$Deaths
data_today$NewIndPositive = data_today$IndPositive - data_yesterday$IndPositive
data_today$NewIndPositive = ifelse(data_today$NewIndPositive >= 0, data_today$NewIndPositive, 0)
data_today$PosTestRate = data_today$NewIndPositive * 100 / data_today$NewIndTested
data_today$ID = county_data$ID[1] + 99:1


county_data$Date = paste(county_data$Year, county_data$Month, county_data$Day, sep = "-")
county_data$Date = as.Date.character(county_data$Date)
county_data = rbind(data_today, county_data)
county_data = county_data[order(ID, decreasing = TRUE)]

for(i in 1:99){
  county = county_data$County[i]
  temp = county_data %>% filter(County == county)
  county_data$PosTestRate14[i] = sum(temp$NewIndPositive[1:14], na.rm = T)/sum(temp$NewIndTested[1:14], na.rm = T)
}


# Update the statewide data
statewide$Date = paste(statewide$Year, statewide$Month, statewide$Day, sep = "-")
statewide$Date = as.Date.character(statewide$Date)
today_statewide = data.frame(today, year(today), month(today), day(today), sum(data_today$IndTested), sum(data_today$IndPositive), sum(data_today$IndRec), sum(data_today$Deaths), sum(data_today$NewIndTested), sum(data_today$NewIndPositive), sum(data_today$NewIndRec), sum(data_today$NewDeaths), 0, statewide$ID[1] + 1, 0)
names(today_statewide) = c("Date","Year", "Month", "Day", "TotalIndTested", "TotalIndPositive", "TotalIndRec", "TotalDeaths", "NewIndTested", "NewIndPositive", "NewIndRec", "NewDeaths", "PosTestRate", "ID", "PosTestRate14")
today_statewide$PosTestRate = today_statewide$NewIndPositive * 100 / today_statewide$NewIndTested
statewide = rbind(setDT(today_statewide), statewide)
statewide = statewide[order(ID, decreasing = TRUE)]
statewide$PosTestRate14[1] = sum(statewide$NewIndPositive[1:14], na.rm = T)/sum(statewide$NewIndTested[1:14], na.rm = T)


# Write out new data
fwrite(data_today, file = today_file)
fwrite(statewide, file = "State_data.csv")
fwrite(county_data, file = "County_data.csv")


