# climate-data-challenge-22
Repository for the Climate Data Challenge, 2022.

## 1. Introduction
This project focuses on thermal discomfort in courtrooms, as one potential impact of climate change on the administration of justice. Climate change poses an increasing risk of overheating buildings, due to increasing outdoor temperatures. At the other extreme, burning fossil fuels to heat cold buildings in winter contributes to climate change, through CO2 emissions. We review the literature on the impacts of weather on court decisions, and propose an investigation based on gaps in the literature.

## 2. Literature Review
There is much literature on the effects of weather on mood and cognition in general, which could both affect decision-making. In particular, a study by Gockel, Kolb and Werth (2014) varied the ambient temperature between 19.9 and 26.8 deg.C and measured the effect on 133 students' judgement of whether a particular crime described to them was murder or manslaughter. Colder temperatures significantly increased the likelihood of judging the crime to be murder.

Heyes and Saberian (2017) found a substantial impact of outdoor temperature on judge decisions in immigration hearings and parole panels in the USA (2000-2004), though in the opposite direction. Out of 207 000 cases analysed, they found a 1.4 %-pt decrease in the granting of asylum or parole for every standard deviation increase in temperature (controlling for rainfall, sunlight hours, pollution and other fixed effects). This amounts to 8.56 % of the current average rate of granting asylum or parole.

Applying a similar methodology to 2.8 million judge decisions in criminal cases in New South Wales (1994-2019), Evans and Siminski (2020) found that outdoor temperature does not have any significant impact on the likelihood of a guilty verdict, nor severity of sentencing.

Drapal and Pina-Sanchez (2019) similarly analysed sentencing decisions in district courts in Prague (2011-2015) and found no significant impact of weather (temperature, pressure, sunshine, wind speed nor humidity) on sentence severity.

Whether this is due to courtrooms in New South Wales and Prague being better insulated against outdoor weather, or some other difference compared to the USA, or particularities in criminal cases that differ from immigration and parole hearings, cannot be concluded definitively.

### Questions
1. How applicable are these findings to the UK, with its particular courtroom building stock?
2. What about the impacts of indoor temperature and humidity, as opposed to outdoor weather?
3. How will any potential impacts project into the future, in a warmer, less predictable climate?
4. Are juries more susceptible to such effects than judges?
5. What other metrics of judicial process effectiveness can be examined, other than guilty verdict likelihood and sentence severity - e.g. duration of crime, likelihood of a decision being appealed, or of an appeal being upheld?
6. What are the implications of increasing remote or virtual participation in trials and hearings?
7. What costs and savings (financial and CO2) would be associated with retrofitting UK court buildings to a standard that minimises unwanted effects on decision-making within them?


## 3. Investigation Proposals
### 3.1 Temperature projections at UK court locations
Greg's work using UKCP climate projections matched up to coordinates of UK court buildings. To produce an animated heat map, and tables of monthly temperature over the next 80 years.

This will be useful no matter what direction the research takes.

### 3.2 Regression of judicial process effectiveness against indoor temperature and humidity
The methods of Heyes and Saberian (2017), Drapal and Pina-Sanchez (2019), and Evans and Siminski (2020) are currently very difficult to apply to a UK setting, as the data required are not readily available in an easily analysable format.

UK court statistics are reported quarterly (https://data.justice.gov.uk/courts/criminal-courts and https://public.tableau.com/app/profile/moj.analysis/viz/CJSScorecard/Introduction) - e.g. percentage of guilty verdicts, effective vs. cracked vs. ineffective cases, time between arrival to completion of cases in a Crown Court.

Data on individual cases in UK courts are very difficult to interpret - e.g. https://tribunalsdecisions.service.gov.uk/utiac?utf8=%E2%9C%93&search%5Bquery%5D=&search%5Breported%5D=true&search%5Bcountry%5D=&search%5Bcountry_guideline%5D=0&search%5Bjudge%5D=&search%5Bclaimant%5D= collects reports on immigration tribunals. Even with natural language processing, legal expertise is needed to train such algorithms - it is not obvious from reading the reports what the outcomes are.

Would like tabulated, e.g.

Case ID | court location | date begin | date end | crime type | verdict | appeal? | appeal upheld?

Ideally we would use indoor temperature and humidity in courtrooms, logged in situ, rather than outdoor weather variables. A methodology inspired by measurements in care homes could be followed https://www.london.gov.uk/sites/default/files/recommendationsreport_carehomeoverheatingauditpilot_200713.pdf
Otherwise we would need to infer indoor temperature based on the state of repair of individual court buildings.

With such data (collected over a number of years), it would be possible to perform a regression analysis to find what relation if any between the independent (building comfort) and dependent (judicial process effectiveness) variables. If significant, the regression coefficients derived could be used to project into the future warming climate, an estimated impact on the dependent variables.


### 3.3 Actions to adapt to and mitigate impacts of thermal discomfort
Already in motion - see https://www.gov.uk/government/news/courts-go-green


## 4. Conclusions


## 5. References

Heyes and Saberian 2017

Evans and Siminski 2020

Gockel, Kolb and Werth 2014

https://data.justice.gov.uk/courts/criminal-courts

https://www.nidirect.gov.uk/articles/attending-court-juror

https://www.gov.uk/government/news/courts-go-green



