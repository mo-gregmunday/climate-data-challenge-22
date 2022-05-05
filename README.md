# climate-data-challenge-22
Repository for the Climate Data Challenge, 2022.

## 1. Introduction
This project focuses on thermal discomfort in courtrooms, as one potential impact of climate change on the administration of justice. Climate change poses an increasing risk of overheating buildings, due to increasing outdoor temperatures. At the other extreme, burning fossil fuels to heat cold buildings in winter contributes to climate change, through CO2 emissions.

In section 2, we review the literature on the impacts of weather on court decisions, identifying questions of interest based on gaps in the knowledge base. In section 3, we propose an investigation to answer some of these questions. Our recommendations are summarised in section 4.

## 2. Literature Review
Summer heatwaves are becoming increasingly common. They are already causing discomfort and disruptions to court proceedings, as reported in the media [1]. In the UK climate, more focus has understandably been placed on heating cold buildings, for example in the care homes sector [2]. There are laudable efforts to improve insulation and energy efficiency in UK court buildings [3] as part of the drive towards net-zero carbon emissions - these efforts  must also take into account the risk of summer overheating in a warming world. As well as the human welfare aspects of thermal comfort, could there be a measurable impact on the administration of justice?

There is much literature on the effects of weather on mood and cognition in general, which could both affect decision-making. In particular, a study by Gockel, Kolb and Werth [4] varied the ambient temperature between 19.9 and 26.8 deg.C and measured the effect on 133 students' judgement of whether a particular crime described to them was murder or manslaughter. Colder temperatures significantly increased the likelihood of judging the crime to be murder.

Heyes and Saberian [5] found a substantial impact of outdoor temperature on judge decisions in immigration hearings and parole panels in the USA (2000-2004), though in the opposite direction. Out of 207 000 cases analysed, they found a 1.4 %-pt decrease in the granting of asylum or parole for every standard deviation increase in temperature (controlling for rainfall, sunlight hours, pollution and other fixed effects). This amounts to 8.56 % of the current average rate of granting asylum or parole.

Applying a similar methodology to 2.8 million judge decisions in criminal cases in New South Wales (1994-2019), Evans and Siminski [6] found that outdoor temperature does not have any significant impact on the likelihood of a guilty verdict, nor severity of sentencing.

Drápal and Pina-Sánchez [7] similarly analysed sentencing decisions in district courts in Prague (2011-2015) and found no significant impact of weather (temperature, pressure, sunshine, wind speed nor humidity) on sentence severity.

Whether this is due to courtrooms in New South Wales and Prague being better insulated against outdoor weather, or some other difference compared to the USA, or particularities in criminal cases that differ from immigration and parole hearings, cannot be concluded definitively.

### Questions
1. How applicable are these findings to the UK, with its particular courtroom building stock?
2. What about the impacts of indoor temperature and humidity, as opposed to outdoor weather?
3. How will any potential impacts project into the future, in a warmer, less predictable climate?
4. Are juries more susceptible to such effects than judges?
5. What other metrics of judicial process effectiveness can be examined, other than guilty verdict likelihood and sentence severity - e.g. duration of crime, likelihood of a decision being appealed, or of an appeal being upheld?
6. What are the implications of increasing remote or virtual participation in trials and hearings?
7. What costs and savings (financial and CO2) would be associated with retrofitting UK court buildings to a standard that minimises unwanted effects on decision-making within them?


## 3. Investigation Proposal
Question 1 (see above) could be answered by following the methods of [5-7], focusing on Crown Court cases that are heard by a jury, in order to contribute towards question 4 as well. However, the data required to apply these methods to a UK context are not readily available in an easily analysable format. Section 3.1 discusses issues with these data and requirements to make the data usable. Section 3.2 describes an analysis that could be performed on such data if it can be collected. Section 3.3 presents one aspect of data that are already available and usable, namely future climate projections. Section 3.4 discusses possible implications of findings from the investigation proposed here.

### 3.1 Issues with available data
UK court statistics are reported quarterly [8-9] - e.g. percentage of guilty verdicts, effective vs. cracked vs. ineffective cases, time between arrival to completion of cases in a Crown Court. These are aggregated rather than individual cases.

Where data on individual cases in UK courts exist, they are very difficult to interpret - e.g. collated reports on immigration tribunals [10]. Even with natural language processing, legal expertise is needed to train such algorithms - it is not obvious from reading the reports what the outcomes are.

Ideally, we would be able to access the data in tabulated form, e.g.

Case ID | court location | date begin | date end | crime type | verdict | sentence | appeal? | appeal upheld?

As well as being more conducive to regression analysis, such data would contribute towards answering question 5 - as well as likelihood of guilty verdict and sentence severity as dependent variables, it would be possible to examine the impacts of weather on other dependent variables:
- duration of trial (subtract "date begin" from "date end")
- likelihood of appeal
- likelihood of successful appeal

The thinking behind these variables is that they may indicate inefficiencies or improper procedure in some way. Though it is not possible to truly quantify something as abstract as the effectiveness of justice, there may also be other proxies worth considering beyond those suggested here.

Question 2 is motivated by the observation that indoor comfort (temperature, humidity) may be more relevant as independent variables than the weather variables examined in [5-7]. They would be related to outdoor weather, but likely strongly dependent on the conditions of each court building. A methodology inspired by measurements in care homes [11] could be followed to log the indoor temperature and humidity in a number of courtrooms, date/time-stamped so they can be matched against court cases and outdoor weather variables that are already being monitored. This would be need to be done over the course of at least one year, to capture seasonal variations.

### 3.2 Regression of judicial process effectiveness against indoor temperature and humidity
With data collected as described above, ideally over a number of years, it would be possible to perform a regression analysis [5-7] to find what relation if any between the independent (building comfort) and dependent (judicial process effectiveness) variables.

Such an analysis should yield estimates of effect size (how strongly do the dependent variables depend on the independent variables) and significance (how likely would these results be obtained by chance, if no relation actually existed, as indicated by p-values).

### 3.3 Temperature projections at UK court locations
Indoor temperature and humidity can be measured in the present-day climate and related to external variables, for example through regression analysis. By deriving regression coefficients (particular to each courtroom), it would be possible to use the UKCP climate projections to estimate the indoor temperature and humidity projected into the future.

With these estimated projections, it would be possible to use the coefficients derived in the separate regression analysis described in section 3.2, to estimate how the metrics of judicial process effectiveness might change in response to climate change.

As a first step towards this, we have produced tabulated time series of temperature and humidity at the locations of all court buildings in the UK. The time series span 80 years at monthly intervals, and are derived from UKCP climate projections RCP 8.5 and .

<img src="courtroom_projections.gif" height="400">
Link to tables.


### 3.4 Actions to adapt to impacts of building discomfort
Note the analysis described above is valid for the case where no changes are made to courtrooms: no retrofitting of window shading, installation of air conditioning, nor behavioural change such as regularly opening windows. The results would be a measure of what should be avoided in future.

Actions to adapt to such conditions are already in motion, as part of an initiative to improve the UK court building stock [3]. One of these adaptations is increased use of video conferencing, which ties in to question 6, above. As well as reducing carbon emissions from transport to and from the courts, remote or hybrid hearings can reduce exposure of participants to the conditions inside the courtrooms - the question then is whether these conditions are better or worse in the buildings from which remote participants join the hearings.

The contribution of the research proposed here is to potentially strengthen the case for adaptation measures in UK court buildings. That is, if an adverse impact on the judicial process due to climate change can be found and confidently quantified, it would further justify the expenditure on retrofitting buildings across the estate: as well as saving CO2 emissions, financial cost on energy bills, and maintaining the health and welfare of participants in the judicial process, there may be a benefit to the effectiveness of the administration of justice. This is an aspect that has not been thoroughly investigated in a UK context so far.

If a null result is found, then far from negating current and future retrofitting efforts, it should provide reassurance that the administration of justice in the UK would not be unduly affected by climate change. The numerous other reasons to work towards net-zero in the courts while respecting human comfort and health within them, all remain valid.


## 4. Conclusions
We recommend the following actions:
- Find some means of collating data on individual court cases into a tabulated form as suggested in section 3.1 - or indeed, begin recording the data in such a way if it has not been done hitherto;
- Bring together currently existing efforts to monitor and record metrics of building comfort such as indoor temperature and humidity - in care homes and prisons as well as courtrooms - to use what has been learned so far to systematise the long-term collection of such data in multiple courtrooms;
- Using such measurements together with existing records of weather variables at court locations, and projections into the future, estimate the expected changes in the building comfort metrics (under the assumption of no adaptation);
- When enough data on building comfort and individual court case judicial process effectiveness has been obtained, perform a regression analysis to identify is there is any correlation;
- If there is significantly, project that forwards to estimate the potential future impact of climate change on the administration of justice;
- Use the findings to direct, inform and justify adaptation measures in UK court buildings.


## 5. References
[1] Kirk, T., "Safety fears over ‘appalling’ heat at Westminster magistrates court", *Evening Standard*, 23 July 2021.
https://www.standard.co.uk/news/uk/westminster-magistrates-court-heatwave-lawyers-defendant-b947410.html

[2] Gupta, R., Barnfield, L., Gregg, M. (2017). "Overheating in care settings: magnitude, causes, preparedness and remedies", *Building Research & Information*, **45**:1-2, 83-101.

[3] GOV.UK, "Courts go green", press release, 7 October 2022. https://www.gov.uk/government/news/courts-go-green

[4] Gockel C., Kolb P.M., Werth L. (2014). "Murder or Not? Cold Temperature Makes Criminals Appear to Be Cold-Blooded and Warm Temperature to Be Hot-Headed." *PLOS ONE* **9**(4): e96231.

[5] Heyes, A., and Saberian, S. (2019). "Temperature and decisions: evidence from 207,000 court cases." *American Economic Journal: Applied Economics* **11.2** (2019): 238-65.

[6] Evans, S., Siminski, P. (2020). "The Effect of Outside Temperature on Criminal Court Sentencing Decisions." *I.Z.A. Institute of Labor Economics*, Discussion Paper 13010.

[7] Drápal, J., Pina-Sánchez, J. (2018). "Does the weather influence sentencing? Empirical evidence from Czech data." *International Journal of Law Crime and Justice.* **56**. 10.1016/j.ijlcj.2018.09.004. 

[8] GOV.UK, "Criminal Courts", accessed 4 May 2022. https://data.justice.gov.uk/courts/criminal-courts

[9] MoJ Analysis, "Criminal Justice System Scorecard", March 2022. https://public.tableau.com/app/profile/moj.analysis/viz/CJSScorecard/Introduction

[10] GOV.UK, "Immigration and asylum chamber: decisions on appeals to the Upper Tribunal", accessed 4 May 2022. https://tribunalsdecisions.service.gov.uk/utiac?utf8=%E2%9C%93&search%5Bquery%5D=&search%5Breported%5D=true&search%5Bcountry%5D=&search%5Bcountry_guideline%5D=0&search%5Bjudge%5D=&search%5Bclaimant%5D=

[11] Oikonomou, E., Raslan, R., Gupta, R., Howard, A., Mavrogianni, A. (2020). "Care Home Overheating Audit Pilot Project - Recommendations Report". *Mayor of London, GLA,
London, UK* . https://www.london.gov.uk/sites/default/files/recommendationsreport_carehomeoverheatingauditpilot_200713.pdf
