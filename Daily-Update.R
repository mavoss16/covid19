library(data.table)
library(ggplot2)
library(lubridate)
library(dplyr)

# Create File Names
today = Sys.Date()
yesterday = Sys.Date() - 1
today_file = paste(month(today), "-", day(today), ".csv", sep = "")
yesterday_file = paste(month(yesterday), "-", day(yesterday), ".csv", sep = "")

file1 = file.path("C:", "Users", "mavos", "OneDrive", "Statistics", "Covid", "Daily-Data", today_file)
file2 = file.path("C:", "Users", "mavos", "OneDrive", "Statistics", "Covid", "Daily-Data", yesterday_file)
file3 = file.path("C:", "Users", "mavos", "OneDrive", "Statistics", "Covid", "State_data.csv")
file4 = file.path("C:", "Users", "mavos", "OneDrive", "Statistics", "Covid", "County_data.csv")


# Get Data
data_today = fread(file1, col.names = c("County", "IndTested", "IndPositive", "IndRec", "Deaths"))
data_yesterday = fread(file2)
county_data = fread(file4)


# Organize the data from today
data_today[, c("Date", "Year", "Month", "Day") := list(today, year(today), month(today), day(today))]
data_today = data_today[order(County)]
data_today = data_today[County != "Pending Investigation"]


# Update county data
data_today = data_today[, c("NewIndTested", "NewIndPositive", "NewIndRec", "NewDeaths", "PosTestRate", "ID") := list(0,0,0,0,0,0)]
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


# Update the statewide data
statewide = fread(file3)
statewide$Date = paste(statewide$Year, statewide$Month, statewide$Day, sep = "-")
statewide$Date = as.Date.character(statewide$Date)
today_statewide = data.frame(today, year(today), month(today), day(today), sum(data_today$IndTested), sum(data_today$IndPositive), sum(data_today$IndRec), sum(data_today$Deaths), sum(data_today$NewIndTested), sum(data_today$NewIndPositive), sum(data_today$NewIndRec), sum(data_today$NewDeaths), 0, statewide$ID[1] + 1)
names(today_statewide) = c("Date","Year", "Month", "Day", "TotalIndTested", "TotalIndPositive", "TotalIndRec", "TotalDeaths", "NewIndTested", "NewIndPositive", "NewIndRec", "NewDeaths", "PosTestRate", "ID")
today_statewide$PosTestRate = today_statewide$NewIndPositive * 100 / today_statewide$NewIndTested
statewide = rbind(setDT(today_statewide), statewide)
statewide = statewide[order(ID, decreasing = TRUE)]


# Write out new data
fwrite(data_today, file = file1)
fwrite(statewide, file = file3)
fwrite(county_data, file = file4)



county_test_rate = function(counties = c("Benton", "Story", "Linn", "Polk")){
  county_data = setDF(county_data)
  temp = county_data %>% filter(County %in%  counties)
  temp$Date = paste(temp$Year, temp$Month, temp$Day, sep = "-")
  temp$Date = as.Date.character(temp$Date)
  temp %>%
    ggplot(aes(x = Date, y = PosTestRate, color = County)) +
    geom_line()
}

state_test_rate = function(){
  statewide = setDF(statewide)
  statewide$Date = paste(statewide$Year, statewide$Month, statewide$Day, sep = "-")
  statewide$Date = as.Date.character(statewide$Date)
  statewide %>%
    ggplot(aes(x = Date, y = PosTestRate)) + geom_line()
}


