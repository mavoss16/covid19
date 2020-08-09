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

