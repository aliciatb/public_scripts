library(shiny)

job <- "Data Scientist, Analytics - Seattle 
Facebook was built to help people connect and share, and over the last decade our tools have played a critical part in changing how people around the world communicate with one another. With over a billion people using the service and more than fifty offices around the globe, a career at Facebook offers countless ways to make an impact in a fast growing organization.
We’re looking for data scientists to work on our core products with a passion for social media to help drive informed business decisions for Facebook. You will enjoy working with one of the richest data sets in the world, cutting edge technology, and the ability to see your insights turned into real products on a regular basis. The perfect candidate will have a background in computer science or a related technical field, will have experience working with large data stores, and will have some experience building software. You are scrappy, focused on results, a self-starter, and have demonstrated success in using analytics to drive the understanding, progression, and user engagement of a product. This position is located in our Seattle office. 
Responsibilities 
Apply your expertise in quantitative analysis, data mining, and the presentation of data to see beyond the numbers and understand how our users interact with our core products
Partner with Product and Engineering teams to solve problems and identify trends and opportunities
Inform, influence, support, and execute our product decisions
Build/maintain reports, dashboards, and metrics to monitor the performance of our products
Mine massive amounts of data and extract useful product insights
Manage development of data resources, gather requirements, organize sources, and support product launches
Requirements 
3+ years experience doing quantitative analysis preferably for a social web company
BA/BS in Computer Science, Math, Physics, or other technical field. Advanced degrees preferred but not required
Fluency in SQL or other programming languages. Some development experience in at least one scripting language (PHP, Python, Perl, etc.)
Experience with large data sets and distributed computing (Hive/Hadoop) a plus
Ability to initiate and drive projects to completion with minimal guidance
The ability to communicate the results of analyses in a clear and effective manner
Basic understanding of statistical analysis, experience with packages such as R, MATLAB, SPSS, SAS, Stata, etc. preferred"
keywords <- "Data Science Shiny"

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