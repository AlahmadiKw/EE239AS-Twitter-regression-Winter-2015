##########################
# Regression Analysis for Tweets 
# 
# Author: Mohammad Mohammad 
# Created on Mar 13 2015 
# Last revision: 
##########################

rm(list=ls())

# import csv data 
dat <- read.table("for_mohammad_only/statistics_#NFL_q3.csv", header=TRUE, sep=',')

# sort by hours (24 hours)
dat <- dat[order(dat$hr),]
hours <- dat$hr 
date_hr <- dat$date_hr

# remove unnessesarry columns
# dat <- data.frame(twt_count = dat$twt_count, flwr_cnt = dat$flwrs_count, ret_cnt = dat$ret_cnt, max_flwrs = dat$max_flwrs, hours = dat$hr)

# assign hr as factors 
# dat$hours <- as.factor(dat$hours)

# remove outliers
dat <- dat[ which(dat$flwrs_count<1e8), ]
dat <- dat[ which(dat$favorite<65), ]
# dat <- dat[ which(dat$hours!=14), ]
# dat <- dat[ which(dat$hours!=16), ]



dat <- aggregate(. ~ hr, 
          mean, 
          data = dat)


# plot scatter 
plot(dat$flwrs_count, dat$twt_count, type="p", lwd=1, col="black", pch=20,
     main="Tweet Count over the number of Followers", ylab="twt_count", xlab="flwrs_count",
     yaxt="n")
plot(dat$hr, dat$twt_count, type="p", lwd=1, col="black", pch=20,
     main="Tweet Count over 24 hrs", ylab="twt_count", xlab="hours",
     yaxt="n")
# identify(dat$hours, dat$twt_count, labels=dat$hours, atpen=TRUE)
plot(dat$ret_cnt, dat$twt_count, type="p", lwd=1, col="black", pch=20,
     main="Tweet Count over retweet sum", ylab="twt_count", xlab="total_retweets",
     yaxt="n")
plot(dat$max_flwrs, dat$twt_count, type="p", lwd=1, col="black", pch=20,
     main="Tweet Count over maximum followers", ylab="twt_count", xlab="max_followers",
     yaxt="n")
plot(dat$momentum, dat$twt_count, type="p", lwd=1, col="black", pch=20,
     main="Tweet Count over maximum followers", ylab="twt_count", xlab="momentum",
     yaxt="n")
plot(dat$favorite, dat$twt_count, type="p", lwd=1, col="black", pch=20,
     main="Tweet Count over favorit", ylab="twt_count", xlab="favorit",
     yaxt="n")
plot(dat$accel, dat$twt_count, type="p", lwd=1, col="black", pch=20,
     main="Tweet Count over acceleration", ylab="twt_count", xlab="acceleration",
     yaxt="n")
plot(dat$peak, dat$twt_count, type="p", lwd=1, col="black", pch=20,
     main="Tweet Count over peak", ylab="twt_count", xlab="peak",
     yaxt="n")
# identify(dat$favorite, dat$twt_count, labels=dat$favorite, atpen=TRUE)

# create predictor
fit <- lm(twt_count ~ flwrs_count + ret_cnt + momentum + peak + accel, dat)  # 1st order linear model 
summary(fit)

# residual plots
# Good model must have a randomly distributed redisual plot. If there is a pattern
# in the plot, the model must be reconsidered 
plot(fit$fit, fit$res, ylab="Residuals", main="residuals against estimated cost")

# leverage 
# outlier test and normality
jack <- rstudent(fit)
plot(jack, ylab="Jacknife Residuals", main="Jacknife Residuals")

# influential obseration test 
cook <- cooks.distance(fit)
plot(cook,ylab="Coocs distance")
influen <- match(cook[cook>.2],cook)
influenctial_data <- dat[influen,]

# assesing normality and outliers as well
qqnorm(fit$res, ylab="Raw Residuals")
qqline(fit$res)
hist(fit$res,10)