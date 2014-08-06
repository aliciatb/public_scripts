setwd("~/public_scripts/worldcup")

# data: http://www.fifa.com/worldcup/statistics/players/distance.html
flags <- read.csv("data/country_codes.csv")
# Or 'alg','arg','aus','bel','bih','bra','civ','cmr','chi','col','crc','cro','ecu','eng','fra','ger','gha','gre','hon','irn','ita','jap','mex','ned','nga','por','rus','kor','esp','sui','uru','usa'

for (code in flags$country_code){
  print(code)
  images_dir = "~/Documents/My Tableau Repository/Shapes/Flags/"
  url = "http://img.fifa.com/images/flags/3/"
  ext = ".png"
  flag_url = paste0(url,code,ext)
  flag_name = paste0(code,ext)
  download.file(flag_url, destfile = paste0(images_dir,flag_name), method = "curl")
}