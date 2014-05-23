# UPDATE FILE LOCATION
user <- read.csv('/Users/luciana/yelp-project/theta.txt', header=F)
rest <- read.csv('/Users/luciana/yelp-project/attrs.txt', header=F)

# k-means
u_cluster <- kmeans(user, 4)$cluster
r_cluster <- kmeans(rest, 2)$cluster
extreme <- min(c(min(user[,1]), min(user[,2]), min(rest[,1]), min(rest[,2])), -max(user[,1]), -max(user[,2]), -max(rest[,1]), -max(rest[,2]))
lim <- c(extreme, -extreme)
plot(1, type='n', xlim=lim, ylim=lim, xlab='Attribute 1', ylab='Attribute 2')
points(user[u_cluster==1,1], user[u_cluster==1,2], col='red')
points(user[u_cluster==2,1], user[u_cluster==2,2], col='blue')
points(user[u_cluster==3,1], user[u_cluster==3,2], col='orange')
points(user[u_cluster==4,1], user[u_cluster==4,2], col='darkgreen')
points(rest[r_cluster==1,1], rest[r_cluster==1,2], pch=2, col='yellow')
points(rest[r_cluster==2,1], rest[r_cluster==2,2], pch=2, col='purple')


# dbscan
library(fpc)
u_cluster <- dbscan(user, 0.2, MinPts=3)$cluster
r_cluster <- dbscan(rest, 1.0, MinPts=3)$cluster
extreme <- min(c(min(user[,1]), min(user[,2]), min(rest[,1]), min(rest[,2])), -max(user[,1]), -max(user[,2]), -max(rest[,1]), -max(rest[,2]))
lim <- c(extreme, -extreme)
plot(1, type='n', xlim=lim, ylim=lim, xlab='Attribute 1', ylab='Attribute 2')
colors = c('red', 'blue', 'green', 'purple', 'orange', 'brown', 'yellow', 'pink', 'deeppink', 'lightblue', 'darkgreen')
for (cluster in unique(u_cluster)) {
 if (cluster == 0)
  color = 'gray'
 else
  color = colors[cluster]
 points(user[u_cluster==cluster,1], user[u_cluster==cluster,2], col=color)
}
for (cluster in unique(r_cluster)) {
 if (cluster == 0)
  color = 'black'
 else
  color = colors[cluster + length(unique(u_cluster))]
 points(rest[r_cluster==cluster,1], rest[r_cluster==cluster,2], col=color, pch=2)
}