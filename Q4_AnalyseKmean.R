## Q4 (jeux de donn?es "stations_metro2.csv")

df <- read.csv("stations_metro2.csv", sep = ";")
X <- scale(df[, c("stop_lat", "stop_lon")])

cl <- kmeans(X, centers = 3)
df$cluster <- cl$cluster

# Visualiser
pairs(X, col = cl$cluster)
table(df$cluster, df$niveau_pollution)
