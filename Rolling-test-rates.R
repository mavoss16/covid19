library(readr)
library(dplyr)
library(magrittr)

statewide = read_csv("State_data.csv")
county_data = read_csv("County_data.csv")

statewide$PosTestRate14 = 0

return_vec = rep(0, length.out = nrow(statewide))
for(i in 1:(nrow(statewide))){
  return_vec[i] = sum(statewide$NewIndPositive[i:(i+13)], na.rm = T)/sum(statewide$NewIndTested[i:(i+13)], na.rm = T)
}

statewide$PosTestRate14 = return_vec


co_return_vec = rep(0, length.out = nrow(county_data))
for(i in 1:99){
  county = county_data$County[i]
  temp = county_data %>% filter(County == county)
  for(j in 1:nrow(temp)){
    position = (99 * (j-1)) + i
    co_return_vec[position] = sum(temp$NewIndPositive[j:(j+13)], na.rm = T)/sum(temp$NewIndTested[j:(j+13)], na.rm = T)
  }
}

county_data$PosTestRate14 = co_return_vec


write_csv(statewide, "State_data.csv")
write_csv(county_data, "County_data.csv")