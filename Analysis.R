library(readr)
library(dplyr)
library(ggplot2)
library(magrittr)
library(leaflet)
library(sf)


# Read in data files
county_data = read_csv("County_data.csv")
statewide = read_csv("State_data.csv")

counties = read_rds("ia_counties.rds")


# Create new date columns
county_data$Date = as.Date.character(paste(county_data$Year, county_data$Month, county_data$Day, sep = "-"))
statewide$Date = as.Date.character(paste(statewide$Year, statewide$Month, statewide$Day, sep = "-"))


counties = left_join(counties %>% mutate(County = NAME), county_data[1:99,])


county_test_rate = function(counties = c("Benton", "Story", "Linn", "Polk")){
  temp = county_data %>% filter(County %in%  counties)
  temp %>%
    ggplot(aes(x = Date, y = PosTestRate, color = County)) +
    geom_line()
}


state_test_rate = function(){
  statewide %>%
    ggplot(aes(x = Date, y = PosTestRate)) + geom_line()
}


rolling_county_test_rate = function(counties = c("Benton", "Story", "Linn", "Polk")){
  temp = county_data %>% filter(County %in%  counties)
  temp %>%
    ggplot(aes(x = Date, y = PosTestRate14, color = County)) +
    geom_line()
}


rolling_state_test_rate = function(){
  statewide %>%
    ggplot(aes(x = Date, y = PosTestRate14)) + geom_line()
}


map_county_rolling = function(){
  scale_range = c(min(counties$PosTestRate14, na.rm = T), max(counties$PosTestRate14, na.rm = T))
  pal = colorNumeric("Blues", scale_range, na.color = "#aaff56")
  
  leaflet() %>%
    addTiles() %>%
    addPolygons(data = st_transform(counties, crs = '+proj=longlat +datum=WGS84'),
                weight = 1, color = "#333333", fillColor = pal(counties$PosTestRate14), fillOpacity = 0.9, label = paste0(counties$County, ", ", round(counties$PosTestRate14, 2))) %>%
    addLegend(position = "topright", pal = pal, values = scale_range, opacity = 0.9,
              title = "14 day<br>positive<br>test rate")  %>%
    setView(lng = -93.119723, lat = 42.156431, zoom = 7)
}


state_deaths = function(type = "Total"){
  if(type == "new"){
    statewide %>%
      ggplot(aes(x = Date, y = NewDeaths)) + geom_line()
  }
  else{
    statewide %>%
      ggplot(aes(x = Date, y = TotalDeaths)) + geom_line()
  }
}

county_deaths = function(counties = c("Benton", "Story", "Linn", "Polk"), type = "total"){
  temp = county_data %>% filter(County %in% counties)
  if(type == "new"){
    temp %>%
      ggplot(aes(x = Date, y = NewDeaths, color = County)) + geom_line()
  }
  else{
    temp %>%
      ggplot(aes(x = Date, y = Deaths, color = County)) + geom_line()
  }
}

