
library(shiny)
library(data.table)
library(wordcloud)
library(ggplot2)
require(RColorBrewer)
pal <- brewer.pal(8,"Accent")

# source: http://norm.al/2009/04/14/list-of-english-stop-words/ 
stopWords <- c('a','about','above','across','after','afterwards','again','against','all','almost','alone','along',
               'already','also','although','always','am','among','amongst','amoungst','amount','an','and','another',
               'any','anyhow','anyone','anything','anyway','anywhere','are','around','as','at','back','be','became',
               'because','become','becomes','becoming','been','before','beforehand','behind','being','below','beside',
               'besides','between','beyond','bill','both','bottom','but','by','call','can','cannot','cant','co','computer',
               'con','could','couldnt','cry','de','describe','detail','do','done','down','due','during','each','eg','eight',
               'either','eleven','else','elsewhere','empty','enough','etc','even','ever','every','everyone','everything',
               'everywhere','except','few','fifteen','fify','fill','find','fire','first','five','for','former','formerly',
               'forty','found','four','from','front','full','further','get','give','go','had','has','hasnt','have','he',
               'hence','her','here','hereafter','hereby','herein','hereupon','hers','him','his','how','however','hundred',
               'i','ie','if','in','inc','indeed','interest','into','is','it','its','itse','keep','last','latter','latterly',
               'least','less','ltd','made','many','may','me','meanwhile','might','mill','mine','more','moreover','most',
               'mostly','move','much','must','my','myse','name','namely','neither','never','nevertheless','next','nine','no',
               'nobody','none','noone','nor','not','nothing','now','nowhere','of','off','often','on','once','one','only','onto',
               'or','other','others','otherwise','our','ours','ourselves','out','over','own','part','per','perhaps','please',
               'put','rather','re','same','see','seem','seemed','seeming','seems','serious','several','she','should','show',
               'side','since','sincere','six','sixty','so','some','somehow','someone','something','sometime','sometimes',
               'somewhere','still','such','system','take','ten','than','that','the','their','them','themselves','then','thence',
               'there','thereafter','thereby','therefore','therein','thereupon','these','they','thick','thin','third','this',
               'those','though','three','through','throughout','thru','thus','to','together','too','top','toward','towards',
               'twelve','twenty','two','un','under','until','up','upon','us','very','via','was','we','well','were','what',
               'whatever','when','whence','whenever','where','whereafter','whereas','whereby','wherein','whereupon','wherever',
               'whether','which','while','whither','who','whoever','whole','whom','whose','why','will','with','within','without',
               'would','yet','you','your','yours','yourself','yourselves')
# stop words data table
stopTerms <- data.table(term=cbind(stopWords))

# stop words added data table for easier checking
stopTerms <- data.table(cbind(stopWords))
setnames(stopTerms,c("stopWords"),c("term"))

jobCloud <- function(job){
  if(nchar(job)>0){
    # scrub job words before running against stopTerms
    clean <- gsub("[^a-zA-Z]", " ", job)
    clean <- gsub(" +", " ", clean)
    clean <- strsplit(clean," ")
    jobTerms <- data.table(term=cbind(tolower(unlist(clean))))
    setnames(jobTerms,c("term.V1"),c("term"))
    
    # keep only terms that are not in stop words
    jobTerms <- jobTerms[!(jobTerms$term %in% stopTerms$term),] 
    
    # calculate frequency of term table
    freqTerms <- data.frame(xtabs(formula = ~., data = jobTerms))
    wordcloud(freqTerms$term,freqTerms$Freq,scale=c(8,.2),min.freq=1,
              random.order=FALSE,use.r.layout=FALSE, 
              rot.per=.15,colors=pal,vfont=c("serif","plain")
    )
  }
}

keywordMatchPlot <- function(keywords,job){
  if(nchar(job) > 0){
    # scrub job words before running against stopTerms
    clean <- gsub("[^a-zA-Z]", " ", job)
    clean <- gsub(" +", " ", clean)
    clean <- strsplit(clean," ")
    jobTerms <- data.table(term=cbind(tolower(unlist(clean))))
    setnames(jobTerms,c("term.V1"),c("term"))
    
    # keep only terms that are not in stop words
    jobTerms <- jobTerms[!(jobTerms$term %in% stopTerms$term),] 
    
    # calculate frequency of term table
    freqTerms <- data.frame(xtabs(formula = ~., data = jobTerms))
    
    dt <- data.table(term=tolower(unlist(strsplit(keywords," "))))
    
    # set default match to zero
    dt$match <- 0
    # if term is in Job Description, set to 1
    dt[dt$term %in% jobTerms$term,match:=1]
    
    # matches
    freqTermsMatch <- merge(dt,freqTerms,by="term")
    # see what % of keywords matched the job description
    matchCount <- nrow(freqTermsMatch)
    if(matchCount>0) matchPercent <- 1 else matchPercent <- 0
    
    # unmatched keyword
    unmatchedWords <- dt[!(dt$term %in% jobTerms$term),]
    if(nrow(unmatchedWords)>0){
      nomatch <- cbind(unmatchedWords,Freq=0)
      freqTermsMatch <- rbind(freqTermsMatch,nomatch)
      noMatchCount <- nrow(unmatchedWords)
      matchPercent <- matchCount/(matchCount+noMatchCount)
    }
    
    freqTermsMatch <- freqTermsMatch[order(freqTermsMatch$Freq,decreasing=TRUE),]
    Terms <- factor(freqTermsMatch$term)
    g <- ggplot(freqTermsMatch,aes(x=term,y=Freq)) 
    print(g + geom_bar(stat='identity') +
            labs(title = paste0(round(matchPercent*100,1),'% match on Keywords')) + 
            labs(x = 'Keyword', y = 'Frequency') +
            theme(plot.title = element_text(face="bold",size=18)) +     
            theme(axis.text.x = element_text(angle=90,face="bold",size="14")) +
            theme(axis.text.y = element_text(face="bold",size="14")) + 
            theme(axis.title = element_text(face="bold",size="16"))
    )
  }
}

shinyServer(
  function(input, output) {
    output$keywordPlot <- renderPlot(keywordMatchPlot({input$keywords},{input$job}))
    output$jobCloud <- renderPlot(jobCloud({input$job}))
  }
)