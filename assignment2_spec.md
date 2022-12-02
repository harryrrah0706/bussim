# Assignment 2 - BusSim

This is a python assignment investigating and improving a bus simulation. You will be completing it in pairs, using git to help you work collaboratively. A starting repository containing the simple model and animation code will be made available on Github.

**Please note we have already made alterations to the assignment to account for the impact of industrial action. No further alterations will be made.**

## Tasks

This assignment comprises of three main tasks:

1. Extending the model. 
2. Analysing the model.
3. Writing a report.

Note that tasks 1 and 2 can be worked upon simultaneously - there is no need to do them in order.

### Task 1: Extending the model

As you should have seen when completing the week 16 worksheet (go complete this if you haven't already!), the current model is very simplistic. For example, buses have no maximum capacity and all the passengers get off at the same stop. We would like you to extend the model to make it more realistic and thus more interesting. There are many ways you could do this, with varying difficulty levels. Here are some examples of what could be done, with an idea of how ambitious they are. Note that this is not an exhaustive list and we encourage creativity.

Less ambitious extensions:

- Maximum passenger capacity on buses.
- Passengers generated with different destinations.
- Passenger pick up times, i.e. a busier bus stop results in the bus taking longer to pick up all the passengers.
- Buses have different speeds.

More ambitious extensions:

- Passenger patience, i.e. how long will they wait for a bus. Grumpy passengers could change colour for example.
- Different routes for buses, i.e. they cater for different stops on the route.

Very ambitious extensions:

- A non-linear bus network. (We recommend you start with a cross shape comprising of one vertical and one horizontal route which share a single stop in the middle.) 
- Adding a cost structure to the model.

### Task 2: Analysing the model

Simulations help us to understand the effects of changing different parameters in our model. Task 2 wants you to investigate the model and create some figures showing interesting behaviour and relationships between parameters. For example, how does the number of buses affect average passenger waiting times? To do this we want you to produce some code which uses the simulation to create data, which is then stored and analysed. You should create two files; one which contains general analysis and plotting functions and another which uses these functions to generate every figure in the report. 

Performance of this task will be assessed on the rigor of parameter searches, difficulty of questions asked and the range and suitability of plot types used. We give some examples below, but again these lists are not exhaustive. Higher marks will be awarded for novelty of questions.

Questions which could be asked:

- How does the number of buses affect the average waiting times of passengers? 
- How do the rates of passenger generation affect the average number of passengers on each bus?
- What is the ideal number of buses in the network under different conditions?

Examples of different plot types we would hope to see include:

- line plots
- scatter plots
- heatmaps
- histograms

### Task 3: Writing the report

The report should be a pdf file no more than 5 pages and consist of the following:

- Introduction
- Explanation of the model and any extensions added.
- Results from the analysis, including figures and discussion. (This should form the bulk of the report.)
- Conclusions and further work. 

A guide on how to write a good report will be released.

## Assessment Criteria

This assignment is worth 25% of the overall module. Marks given will be out of 100, and weighted accordingly:

- 30 marks: Task 1: Extensions of the model.
- 30 marks: Task 2: Analysis of the model
- 10 marks: Collaborative use of git. 
    - Are commit messages sensible?
    - Are efforts being made to avoid merge conflicts? Occasional merge conflicts are fine when resolved sensibly, this is just a repercussion of collaborative working. However, many merge conflicts in a row indicate incorrect usage of git.
    - Do commits show incremental changes rather than large scale alterations happening all at once? 
- 15 marks: Code quality.  
    - Any extensions to the code should stick to the styling already there with respect to variables names and conventions.
    - Comments.
    - General good practices of writing python.
- 15 marks: Report quality.
    - Good academic English should be used throughout.
    - Figures should have titles, axes labels and legends (where appropriate).
    - All figures should have a caption and also be explained and discussed in the main text of the report.
    - Pseudocode should be used if referencing code. No screen shots of code.
    - A more comprehensive guide to writing a good report will be released.

### Examples projects and projected grades:

Here are some examples of how we would grade some example projects. Note this is in no way prescriptive, but just meant as a rough guide. We recommend everyone starts by attempting some of the less ambitious extensions.

- Project A: **2:2**
    - Completed three extensions from the less ambitious list.
    - Three questions analysed from the given list. Two different plot types used.
    - Good code and report quality.
    - Some sensible git use shown, but many unnecessary merge conflicts, indicating correct collaborative workflow was not used.

- Project B: **2:1**
    - Completed two extensions from the less ambitious list and one from the more ambitious list.
    - Four questions analysed, three of which were novel. Three different plot types used, with multiple plot types being used to answer a different aspect of the same question.
    - Excellent code and report quality.
    - Good use of collaborative git.

- Project C: **1:1**
    - Completed multiple of the more ambitious extensions, possibly novel. 
    **OR** 
    Completed one of the very ambitious extensions (or novel alternative). 
    - Four questions analysed - all of which are novel. Some incorporate the extensions. Many different plots are used, with thought given to the best plot to represent the data. Clear understanding of plotting shown, with care taken over formatting. Subplots used.
    - Excellent code and report quality.
    - Good use of collaborative git.

## Working in pairs

This assignment requires you to work collaboratively as a pair. You can either choose to do this by splitting the tasks between yourselves or working on both tasks together. The tasks have been structured in such a way that they share little dependence. If you have any trouble working with your partner, please inform us as soon as possible so that we can help resolve any issues. Note that git makes the distribution of workload completion clear.

## Submission

The deadline for submission will be **Tuesday 10th March at noon**. 

Once again submission will be through Github Classroom and you need to make sure that your final changes have been pushed to the repository before the deadline. Your report should be included as a pdf in the repository and the README.md file should be adapted to reflect any extensions made to the model and detail how to generate the figures used in the report. This should be possible by running a single python script - Markers will not be delving into code to see how to generate figures.

Please make sure that you do not collaborate between teams. It is fine to discuss ideas with each other, but **code will be checked for plagiarism** and this includes between teams.