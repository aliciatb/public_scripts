# install.packages("devtools")
# devtools::install_github('rstudio/shinyapps')
# devtools::install_github("rstudio/shiny-incubator")

install.packages("RColorBrewer")

appName <- "jobcloud"

library(shiny)
setwd(paste0("~/public_scripts/",appName)
# runApp(appName)
runApp(appName, display.mode = "showcase")

# deploy
library(shinyapps)
setwd("/public_scripts")
deployApp()