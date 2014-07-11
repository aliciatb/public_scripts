library(shiny)

job <- "Data Visualization Engineer 

Brightcove - Seattle, WA 

Brightcove's Video Cloud product is the industry leading online video platform for media and marketing. Our customers range from corporate product marketers to large non-profit organizations to major media publishers.

We are looking for a data visualization engineer to work on our analytics team. The analytics platform has vast amounts of data available detailing more than 200 years of video consumption per day. We want an engineer who can design intuitive visualizations of video consumption data for Brightcove customers, and then implement those designs using HTML5. 

ABOUT THE TEAM:
The team you'll be joining is a small, self-organized Agile group focused on solving hard engineering problems. Brightcove is full of truly talented software professionals who love their craft. We use an agile process that ensures the features we build will delight our customers *and* that we're usually home in time for dinner. We are always shipping code -- even several times a day. The team consists of developers who double as experts in operating the systems that they build, take pride in our extremely high uptime stats and our software quality.

Desired Skills and Experience
ABOUT YOU:
You have experience designing data visualizations including user interface design, and HTML5 implementation skills. You have an interest in big data, maybe you think of yourself as a data scientist.

You have experience developing and deploying software at high scale.

You understand the principles of software craftsmanship. You write clean code, even when working on extremely hard problems. You think about how your code will be maintained and tested.

You are self-motivated, proactive, curious, responsible and flexible.

WHAT WE LOOK FOR IN ALL NEW EMPLOYEES:
People we can learn from!
People who are creative, passionate, and curious!
People who are nice, and want to get things done!"
keywords <- "Data Science SQL R Tableau"

# 3rd example
shinyUI(pageWithSidebar(
  headerPanel("Visualize your next Job!"),
  sidebarPanel(
    textInput("job", "Enter Job Description:", job),
    textInput("keywords", "Enter Keywords for job:", keywords),
    h4('Job Description'),
    verbatimTextOutput("jobDescription")
  ),
  mainPanel(
    h3('Word Cloud of the Job Description'),
    p('Visual representation of the words where the larger the size of the font, the more frequently that term appeared in the description.'),
    p('Note that common "stop" words (a, an, and, the, or, etc.) were not included in the cloud.'),
    plotOutput('jobCloud'),
    h3('Frequency of Keywords in the Job Description'),
    p('Barplot with percentage of match on key words found in the job description.'),
    plotOutput('keywordPlot')
  )
)
)