# processcfbfile("cfbstats.com-2013-1.5.20",)
processcfbfile <- function(folder){
#   setwd("/Users/aliciabrown/scripts/public/cfb")
  setwd("/Users/aliciatb/scripts/public/cfb") 

  # load packages
  library(plyr)
  
  ## Read football data (source = http://www.cfbstats.com/blog/college-football-data/)
  dir <- "~/data/cfb/"
  team <- read.csv(paste0(dir,folder, "/team.csv"), colClasses = "character")
  conference <- read.csv(paste0(dir,folder, "/conference.csv"), colClasses = "character")
  teamgamestats <- read.csv(paste0(dir,folder, "/team-game-statistics.csv"), colClasses = "character")
  
  # 1 row per team per game
  gamescores <- teamgamestats[, c("Game.Code", "Team.Code", "Points")]
  gamescores <- with(gamescores, gamescores[order(Game.Code,as.numeric(Points)), ])
  
  scores <- data.frame(Game.Code = character(0), Team.Code.1 = character(0), Points.1 = numeric(0), Team.Code.2 = character(0), Points.2 = numeric(0), Team.Winner = character(0), stringsAsFactors=F)
  lastrow <- 0
  for(n in 1:(nrow(gamescores)/2)){
    scores[n,1] <- as.character(gamescores[lastrow + 1,1])
    scores[n,2] <- gamescores[lastrow + 1,2]
    scores[n,3] <- gamescores[lastrow + 1,3]
    scores[n,4] <- gamescores[lastrow + 2,2]
    scores[n,5] <- gamescores[lastrow + 2,3]
    # while it appears that 2nd team is winner, should calculate this just to be sure in case data file format ever changes
    scores[n,6] <- gamescores[lastrow + 2,2]
    lastrow <- lastrow + 2
  }
  # check the data
  # aggie.wins <- subset(scores, scores[,6]=="697")
  # alabama.wins <- subset(scores, scores[,6]=="8")
  
  team.Wins <- count(scores,c(Team.Code="Team.Winner"))
  team.Wins <- rename(team.Wins, c("freq" = "Wins"))
  
  all.teams.win.count <- merge(team, team.Wins, by = "Team.Code", all = TRUE)
  #set NAs to 0 and now we have all teams with Win count
  all.teams.win.count[is.na(all.teams.win.count)] <- 0
  
  # add conference and division
  all.teams.win.count <- merge(all.teams.win.count,conference,by="Conference.Code", all = TRUE)
  all.teams.win.count <- rename(all.teams.win.count, c("Name.x"="Name","Name.y"="Conference"))
  
  # validate team win counts
  msg <- paste("Team count (", nrow(team), ") and all.teams.win.count (", nrow(all.teams.win.count), ") do not equal same #")
  if(nrow(team) != nrow(all.teams.win.count)){
    #print(msg)
    stop(msg) 
  }
  
  # files with TD data
  game <- read.csv(paste0(dir,folder,"/game.csv"), colClasses = "character")
  pass <- read.csv(paste0(dir,folder,"/pass.csv"), colClasses = "character")
  rush <- read.csv(paste0(dir,folder,"/rush.csv"), colClasses = "character")
  
  # filter on TDs plays
  rush.TD <- subset(rush, rush$Touchdown == 1, select = c("Game.Code", "Play.Number", "Team.Code", "Touchdown"))
  pass.TD <- subset(pass, pass$Touchdown == 1, select = c("Game.Code", "Play.Number", "Team.Code", "Touchdown"))
  
  team.rush.TD <- merge(team, rush.TD, by = "Team.Code", all = FALSE)
  team.pass.TD <- merge(team, pass.TD, by = "Team.Code", all = FALSE)
  
  # check our data against http://espn.go.com/college-football/statistics/team/_/stat/passing & http://espn.go.com/college-football/statistics/team/_/stat/rushing & passing
  # Team.Code  Name         Conference.Code
  # 697        Texas A&M    911
  # 8          Alabama	    911
  # aggies.rush.TD <- subset(team.rush.TD, team.rush.TD$Team.Code == 697)
  # tide.rush.TD <- subset(team.rush.TD, team.rush.TD$Team.Code == 8)
  # aggies.pass.TD <- subset(team.pass.TD, team.pass.TD$Team.Code == 697)
  # tide.pass.TD <- subset(team.pass.TD, team.pass.TD$Team.Code == 8)
  
  team.TD <- rbind(team.rush.TD, team.pass.TD)
  
  # validate sum of TDs
  if(nrow(team.TD) != (nrow(team.rush.TD) + nrow(team.pass.TD))){
    stop("team.TD count does not add up to team.rush.TD plus team.pass.TD!")
#     print("team.TD count does not add up to team.rush.TD plus team.pass.TD!")
  }
  
  # merge wins and total TDs in order to validate numbers
  all.team.TD <- count(team.TD,c("Team.Code","Name"))
  all.team.TD <- rename(all.team.TD, c("freq"="Touchdowns"))
  all.teams.win.TD.count <- merge(all.teams.win.count, all.team.TD, by = "Team.Code", all.x = TRUE)
  all.teams.win.TD.count <- rename(all.teams.win.TD.count, c("Name.x"="Name"))
  all.teams.win.TD.count <- all.teams.win.TD.count[,c("Team.Code",  "Name",	"Conference", "Subdivision", "Wins", "Touchdowns")]
  all.teams.win.TD.count[is.na(all.teams.win.TD.count)] <- 0
  
  # validate team counts
  msg <- paste("Team count (", nrow(team), ") and all.teams.win.TD.count (", nrow(all.teams.win.TD.count), ") do not equal same #")
  if(nrow(team) != nrow(all.teams.win.TD.count)){
#     print(msg)
    stop(msg) 
  }
  
  # Correlational analysis
  # cor(all.teams.win.TD.count[4:5])
  # cor.test(all.teams.win.TD.count$Wins, all.teams.win.TD.count$Touchdowns)
  
  play <- read.csv(paste0(dir,folder,"/play.csv"), colClasses = "character")
  
  # Todo: should write function to handle each play data since there's a lot of mostly duplicated code below
  
  # filter TD plays on downs
  play.1st <- subset(play, play$Down == 1 & play$Play.Type %in% c("PASS", "RUSH"), select = c(Game.Code, Offense.Team.Code, Defense.Team.Code, Play.Number, Distance, Spot, Play.Type))
  play.2nd <- subset(play, play$Down == 2 & play$Play.Type %in% c("PASS", "RUSH"), select = c(Game.Code, Offense.Team.Code, Defense.Team.Code, Play.Number, Distance, Spot, Play.Type))
  play.3rd <- subset(play, play$Down == 3 & play$Play.Type %in% c("PASS", "RUSH"), select = c(Game.Code, Offense.Team.Code, Defense.Team.Code, Play.Number, Distance, Spot, Play.Type))
  play.4th <- subset(play, play$Down == 4 & play$Play.Type %in% c("PASS", "RUSH"), select = c(Game.Code, Offense.Team.Code, Defense.Team.Code, Play.Number, Distance, Spot, Play.Type))
  
  # join on completed games
  game.TD <- merge(game, team.TD, by = "Game.Code", all = FALSE)
  
  # merge TDs with plays
  TD.1st <- merge(play.1st, game.TD, by = c("Game.Code", "Play.Number"), all = FALSE)
  TD.2nd <- merge(play.2nd, game.TD, by = c("Game.Code", "Play.Number"), all = FALSE)
  TD.3rd <- merge(play.3rd, game.TD, by = c("Game.Code", "Play.Number"), all = FALSE)
  TD.4th <- merge(play.4th, game.TD, by = c("Game.Code", "Play.Number"), all = FALSE)
  # order this
  TD.1st <- with(TD.1st, TD.1st[order(Name,Date,as.numeric(Play.Number)), ])
  TD.2nd <- with(TD.2nd, TD.2nd[order(Name,Date,as.numeric(Play.Number)), ])
  TD.3rd <- with(TD.3rd, TD.3rd[order(Name,Date,as.numeric(Play.Number)), ])
  TD.4th <- with(TD.4th, TD.4th[order(Name,Date,as.numeric(Play.Number)), ])
  
  # validate sum of TDs
  if(nrow(team.TD) != (nrow(TD.1st) + nrow(TD.2nd) + nrow(TD.3rd) + nrow(TD.4th))){
    stop("team.TD count does not add up to Touchdowns by Down Count!")
#     print("team.TD count does not add up to Touchdowns by Down Count!")
#     print(paste0("team.TD=",nrow(team.TD)))
#     print(paste0("TD.1st=",nrow(TD.1st)))
#     print(paste0("TD.2nd=",nrow(TD.2nd)))
#     print(paste0("TD.3rd=",nrow(TD.3rd)))
#     print(paste0("TD.4th=",nrow(TD.4th)))
#     print(paste0(nrow(team.TD),"-",nrow(TD.1st) + nrow(TD.2nd) + nrow(TD.3rd) + nrow(TD.4th),"=",nrow(team.TD)-(nrow(TD.1st) + nrow(TD.2nd) + nrow(TD.3rd) + nrow(TD.4th))))
  }
  
  data <- TD.1st[,c("Offense.Team.Code","Name","Date","Game.Code", "Play.Type", "Spot","Distance", "Defense.Team.Code", "Touchdown")]
  team.1st.TD.Count <- count(data, c("Name","Offense.Team.Code"))
  team.1st.TD.Count <- rename(team.1st.TD.Count, c("Offense.Team.Code"="Team.Code","freq"="First.Down.TD"))
  
  data <- TD.2nd[,c("Offense.Team.Code","Name","Date","Game.Code", "Play.Type", "Spot","Distance", "Defense.Team.Code", "Touchdown")]
  team.2nd.TD.Count <- count(data, c("Name","Offense.Team.Code"))
  team.2nd.TD.Count <- rename(team.2nd.TD.Count, c("Offense.Team.Code"="Team.Code","freq"="Second.Down.TD"))
  
  data <- TD.3rd[,c("Offense.Team.Code","Name","Date","Game.Code", "Play.Type", "Spot","Distance", "Defense.Team.Code", "Touchdown")]
  team.3rd.TD.Count <- count(data, c("Name","Offense.Team.Code"))
  team.3rd.TD.Count <- rename(team.3rd.TD.Count, c("Offense.Team.Code"="Team.Code","freq"="Third.Down.TD"))
  
  data <- TD.4th[,c("Offense.Team.Code","Name","Date","Game.Code", "Play.Type", "Spot","Distance", "Defense.Team.Code", "Touchdown")]
  team.4th.TD.Count <- count(data, c("Name","Offense.Team.Code"))
  team.4th.TD.Count <- rename(team.4th.TD.Count, c("Offense.Team.Code"="Team.Code","freq"="Fourth.Down.TD"))
  
  # merge Down TDs with Wins by Team
  all.teams.win.TD.count <- merge(all.teams.win.TD.count, team.1st.TD.Count, by = "Team.Code", all = TRUE)
  all.teams.win.TD.count <- rename(all.teams.win.TD.count, c("Name.x"="Name"))
  all.teams.win.TD.count <- all.teams.win.TD.count[,c("Team.Code", "Name", "Conference", "Subdivision", "Wins", "First.Down.TD", "Touchdowns")]
  
  all.teams.win.TD.count <- merge(all.teams.win.TD.count, team.2nd.TD.Count, by = "Team.Code", all = TRUE)
  all.teams.win.TD.count <- rename(all.teams.win.TD.count, c("Name.x"="Name"))
  all.teams.win.TD.count <- all.teams.win.TD.count[,c("Team.Code", "Name", "Conference", "Subdivision", "Wins", "First.Down.TD", "Second.Down.TD", "Touchdowns")]
  
  all.teams.win.TD.count <- merge(all.teams.win.TD.count, team.3rd.TD.Count, by = "Team.Code", all = TRUE)
  all.teams.win.TD.count <- rename(all.teams.win.TD.count, c("Name.x"="Name"))
  all.teams.win.TD.count <- all.teams.win.TD.count[,c("Team.Code", "Name", "Conference", "Subdivision", "Wins", "First.Down.TD", "Second.Down.TD", "Third.Down.TD","Touchdowns")]
  
  all.teams.win.TD.count <- merge(all.teams.win.TD.count, team.4th.TD.Count, by = "Team.Code", all = TRUE)
  all.teams.win.TD.count <- rename(all.teams.win.TD.count, c("Name.x"="Name"))
  all.teams.win.TD.count <- all.teams.win.TD.count[,c("Team.Code", "Name", "Conference", "Subdivision", "Wins", "First.Down.TD", "Second.Down.TD", "Third.Down.TD", "Fourth.Down.TD", "Touchdowns")]
  
  all.teams.win.TD.count[is.na(all.teams.win.TD.count)] <- 0
  # order by Name
  all.teams.win.TD.count <- with(all.teams.win.TD.count, all.teams.win.TD.count[order(Name), ])
  
  # need tableau-friendly file names
  outputName <- sub("cfbstats.com-2013-1.5.","2013cfbweek",folder)
  outputName <- paste0(dir,outputName)
  
  # output to csv
  write.csv(all.teams.win.TD.count, file = paste0(outputName,"touchdowns.csv"), row.names = FALSE)
  # Correlational analysis
  cor(all.teams.win.TD.count[5:10])
  
  # group other team stats to compare against teamgamestats
  # Team.Code Game.Code Points Third.Down.Att Third.Down.Conv Fourth.Down.Att Fourth.Down.Conv
  # Red.Zone.Att Red.Zone.TD Red.Zone.Field.Goal Field.Goal.Att Field.Goal.Made Punt Punt.Yard
  # Time.Of.Possession Penalty Penalty.Yard
  team.Conversions <- ddply(teamgamestats,~Team.Code,summarise,Third.Down.Conv=sum(as.numeric(Third.Down.Conv)),Fourth.Down.Conv=sum(as.numeric(Fourth.Down.Conv)),Red.Zone.TD=sum(as.numeric(Red.Zone.TD)),Red.Zone.Field.Goal=sum(as.numeric(Red.Zone.Field.Goal)), .drop = FALSE)
  team.stats.all <- merge(all.teams.win.TD.count, team.Conversions, by = "Team.Code", all = TRUE)
  team.stats <- merge(all.teams.win.TD.count, team.Conversions, by = "Team.Code", all = FALSE)
  team.stats.all <- with(team.stats.all, team.stats.all[order(Name), ])
  team.stats <- with(team.stats, team.stats[order(Name), ])
  
  # output to csv
  write.csv(team.stats.all, file = paste0(outputName,"expandedStatsWithNAs.csv"), row.names = FALSE)
  write.csv(team.stats, file = paste0(outputName,"expandedStats.csv"), row.names = FALSE)
  # time for stats!
  
  # Correlational analysis
  stats <- cor(team.stats[5:14])
  
  # NHST for each correlation coefficient
  cor.test(team.stats$Wins, team.stats$Red.Zone.TD)
  cor.test(team.stats$Wins, team.stats$Fourth.Down.TD)
  cor.test(team.stats$Wins, team.stats$Third.Down.TD)
  cor.test(team.stats$Wins, team.stats$Second.Down.TD)
  cor.test(team.stats$Wins, team.stats$First.Down.TD)

  return(stats)
}