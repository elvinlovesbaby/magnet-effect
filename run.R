


data <- read.csv('csv/sh600000__down__2015-01-19.csv',
                 header = F,
                 sep = ',',
                 stringsAsFactors = F)

print(summary(data))

col_num = ncol(data)
row_num = nrow(data)

plot(x = c(1:row_num), y = data[,2])
