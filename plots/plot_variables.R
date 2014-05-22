# UPDATE FILE LOCATION
user <- read.csv('/Users/luciana/yelp-project/theta.txt', header=F)
rest <- read.csv('/Users/luciana/yelp-project/attrs.txt', header=F)
u_cluster <- kmeans(user, 2)$cluster
r_cluster <- kmeans(rest, 2)$cluster
extreme <- min(c(min(user[,1]), min(user[,2]), min(rest[,1]), min(rest[,2])), -max(user[,1]), -max(user[,2]), -max(rest[,1]), -max(rest[,2]))
lim <- c(extreme, -extreme)
plot(1, type='n', xlim=lim, ylim=lim, xlab='Attribute 1', ylab='Attribute 2')
points(user[u_cluster==1,1], user[u_cluster==1,2], col='red')
points(user[u_cluster==2,1], user[u_cluster==2,2], col='blue')
points(rest[r_cluster==1,1], rest[r_cluster==1,2], pch=2, col='green')
points(rest[r_cluster==2,1], rest[r_cluster==2,2], pch=2, col='purple')
