
install.packages("readODS")
install.packages("logistf")
install.packages("multcomp")
install.packages("survival")
library(survival)
library(multcomp)
library(readODS)
library(logistf)
data <- read.csv("C:\\Users\\SH\\Documents\\random_10.csv")
names(data) <- c("Rule", "Axiom", "Profile", "Score")
##Compute scores

ScorePluralityUnanonimity <- data$Score[data$Axiom==0 & data$Rule==0]
ScorePluralityCommittee <- data$Score[data$Axiom==1 & data$Rule==0]
ScorePluralityMinority <- data$Score[data$Axiom==2 & data$Rule==0]
ScorePluralityRegret <- data$Score[data$Axiom==3 & data$Rule==0]
ScorePluralityCopeland <- data$Score[data$Axiom==4 & data$Rule==0]
ScorePluralityGini <- data$Score[data$Axiom==5 & data$Rule==0]
ScorePluralityNew <- data$Score[data$Axiom==6 & data$Rule==0]

ScoreBordaUnanonimity <- data$Score[data$Axiom==0 & data$Rule==1]
ScoreBordaCommittee <- data$Score[data$Axiom==1 & data$Rule==1]
ScoreBordaMinority <- data$Score[data$Axiom==2 & data$Rule==1]
ScoreBordaRegret <- data$Score[data$Axiom==3 & data$Rule==1]
ScoreBordaCopeland <- data$Score[data$Axiom==4 & data$Rule==1]
ScoreBordaGini <- data$Score[data$Axiom==5 & data$Rule==1]
ScoreBordaNew <- data$Score[data$Axiom==6 & data$Rule==1]

ScoreCopelandUnanonimity <- data$Score[data$Axiom==0 & data$Rule==2]
ScoreCopelandCommittee <- data$Score[data$Axiom==1 & data$Rule==2]
ScoreCopelandMinority <- data$Score[data$Axiom==2 & data$Rule==2]
ScoreCopelandRegret <- data$Score[data$Axiom==3 & data$Rule==2]
ScoreCopelandCopeland <- data$Score[data$Axiom==4 & data$Rule==2]
ScoreCopelandGini <- data$Score[data$Axiom==5 & data$Rule==2]
ScoreCopelandNew <- data$Score[data$Axiom==6 & data$Rule==2]

ScoreKnapsackUnanonimity <- data$Score[data$Axiom==0 & data$Rule==3]
ScoreKnapsackCommittee <- data$Score[data$Axiom==1 & data$Rule==3]
ScoreKnapsackMinority <- data$Score[data$Axiom==2 & data$Rule==3]
ScoreKnapsackRegret <- data$Score[data$Axiom==3 & data$Rule==3]
ScoreKnapsackCopeland <- data$Score[data$Axiom==4 & data$Rule==3]
ScoreKnapsackGini <- data$Score[data$Axiom==5 & data$Rule==3]
ScoreKnapsackNew <- data$Score[data$Axiom==6 & data$Rule==3]

ScoreThetaUnanonimity <- data$Score[data$Axiom==0 & data$Rule==4]
ScoreThetaCommittee <- data$Score[data$Axiom==1& data$Rule==4]
ScoreThetaMinority <- data$Score[data$Axiom==2 & data$Rule==4]
ScoreThetaRegret <- data$Score[data$Axiom==3 & data$Rule==4]
ScoreThetaCopeland <- data$Score[data$Axiom==4 & data$Rule==4]
ScoreThetaGini <- data$Score[data$Axiom==5 & data$Rule==4]
ScoreThetaNew <- data$Score[data$Axiom==6 & data$Rule==4]


ScoreBordaUnanonimity <- data$Score[data$Axiom==0 & data$Rule==1]
ScoreBordaCommittee <- data$Score[data$Axiom==1 & data$Rule==1]
ScoreBordaMinority <- data$Score[data$Axiom==2 & data$Rule==1]
ScoreBordaRegret <- data$Score[data$Axiom==3 & data$Rule==1]
ScoreBordaCopeland <- data$Score[data$Axiom==4 & data$Rule==1]
ScoreBordaGini <- data$Score[data$Axiom==5 & data$Rule==1]
ScoreBordaNew <- data$Score[data$Axiom==6 & data$Rule==1]

MeanScoreCopelandUnanonimity <- mean(data$Score[data$Axiom==0 & data$Rule==2])
MeanScoreCopelandCommittee <- mean(data$Score[data$Axiom==1 & data$Rule==2])
MeanScoreCopelandMinority <- mean(data$Score[data$Axiom==2 & data$Rule==2])
MeanScoreCopelandRegret <- mean(data$Score[data$Axiom==3 & data$Rule==2])
MeanScoreCopelandCopeland <- mean(data$Score[data$Axiom==4 & data$Rule==2])
MeanScoreCopelandGini <- mean(data$Score[data$Axiom==5 & data$Rule==2])
MeanScoreCopelandNew <- mean(data$Score[data$Axiom==6 & data$Rule==2])

MeanScoreKnapsackUnanonimity <- mean(data$Score[data$Axiom==0 & data$Rule==3])
MeanScoreKnapsackCommittee <- mean(data$Score[data$Axiom==1 & data$Rule==3])
MeanScoreKnapsackMinority <- mean(data$Score[data$Axiom==2 & data$Rule==3])
MeanScoreKnapsackRegret <- mean(data$Score[data$Axiom==3 & data$Rule==3])
MeanScoreKnapsackCopeland <- mean(data$Score[data$Axiom==4 & data$Rule==3])
MeanScoreKnapsackGini <- mean(data$Score[data$Axiom==5 & data$Rule==3])
MeanScoreKnapsackNew <- mean(data$Score[data$Axiom==6 & data$Rule==3])

MeanScoreThetaUnanonimity <- mean(data$Score[data$Axiom==0 & data$Rule==4])
MeanScoreThetaCommittee <- mean(data$Score[data$Axiom==1& data$Rule==4])
MeanScoreThetaMinority <- mean(data$Score[data$Axiom==2 & data$Rule==4])
MeanScoreThetaRegret <- mean(data$Score[data$Axiom==3 & data$Rule==4])
MeanScoreThetaCopeland <- mean(data$Score[data$Axiom==4 & data$Rule==4])
MeanScoreThetaGini <- mean(data$Score[data$Axiom==5 & data$Rule==4])
MeanScoreThetaNew <- mean(data$Score[data$Axiom==6 & data$Rule==4])

## Plot

plotCommittee <-barplot(c(
mean(ScorePluralityCommittee),
mean(ScoreBordaCommittee),
MeanScoreCopelandCommittee,
MeanScoreKnapsackCommittee,
MeanScoreThetaCommittee),
names.arg=c("Plurality", "Borda", "Copeland", "Knapsack", "Theta"),
main="Committee", col=hcl(h = 0, c = 35, l = 85,  fixup = TRUE))

plotMinority <-barplot(c(mean(ScorePluralityMinority), mean(ScoreBordaMinority), MeanScoreCopelandMinority, MeanScoreKnapsackMinority, MeanScoreThetaMinority),  names.arg=c("Plurality", "Borda", "Copeland", "Knapsack", "Theta"), main="Minority")
plotRegret <-barplot(c(mean(ScorePluralityRegret), mean(ScoreBordaRegret), MeanScoreCopelandRegret, MeanScoreKnapsackRegret, MeanScoreThetaRegret),  names.arg=c("Plurality", "Borda", "Copeland", "Knapsack", "Theta"), main="Regret")
plotCopeland <-barplot(c(mean(ScorePluralityCopeland), mean(ScoreBordaCopeland), MeanScoreCopelandCopeland, MeanScoreKnapsackCopeland, MeanScoreThetaCopeland),  names.arg=c("Plurality", "Borda", "Copeland", "Knapsack", "Theta"), main="Copeland")
plotGini <-barplot(c(mean(ScorePluralityGini), mean(ScoreBordaGini), MeanScoreCopelandGini, MeanScoreKnapsackGini, MeanScoreThetaGini),  names.arg=c("Plurality", "Borda", "Copeland", "Knapsack", "Theta"), main="Gini")
fd##Analysis prep
data_Committee <- data[data$Axiom==1,]
data_Minority <- data[data$Axiom==2,]
data_Regret <- data[data$Axiom==3,]
data_Copeland <- data[data$Axiom==4,]
data_Gini <- data[data$Axiom==5,]
data_New <- data[data$Axiom==6,]

RulesComm <- factor(data_Committee$Rule)
RulesMin <- factor(data_Minority$Rule)
RulesReg <- factor(data_Regret$Rule)
RulesCop <- factor(data_Copeland$Rule)
RulesGini <- factor(data_Gini$Rule)
RulesNew <- factor(data_New$Rule)
##Analysis ANOVA Ax1
Rules <- factor(data_Committee$Rule)
anovaCommittee <- aov(Score ~ RulesComm, data=data_Committee)
anovaMinority <- aov(Score ~ RulesMin, data=data_Minority)
anovaRegret <- aov(Score ~ RulesReg, data=data_Regret)
anovaCopeland <- aov(Score ~ RulesCop, data=data_Copeland)
anovaGini  <- aov(Score ~ RulesGini, data=data_Gini )
anovaNew  <- aov(Score ~ RulesNew, data=data_New )

##Posthoc analysis

posthocCommittee <- TukeyHSD(anovaCommittee)
posthocMinority <- TukeyHSD(anovaMinority)
posthocRegret <- TukeyHSD(anovaRegret)
posthocCopeland <- TukeyHSD(anovaCopeland)
posthocGini <- TukeyHSD(anovaGini)
posthocNew <- TukeyHSD(anovaNew)

posthocCommittee99 <- TukeyHSD(anovaCommittee, conf.level = 0.99)
posthocMinority99 <- TukeyHSD(anovaMinority, conf.level = 0.99)
posthocRegret99 <- TukeyHSD(anovaRegret, conf.level = 0.99)
posthocCopeland99 <- TukeyHSD(anovaCopeland, conf.level = 0.99)
posthocGini99 <- TukeyHSD(anovaGini, conf.level = 0.99)
posthocNew99 <- TukeyHSD(anovaNew, conf.level = 0.99)

##Analysis logistic regression

LogisticCommittee <- glm(formula = Score ~ RulesComm, data=data_Committee, family = binomial)
LogisticMinority <- glm(formula = Score ~ RulesMin, data=data_Minority, family = binomial)
LogisticRegret <- glm(formula = Score ~ RulesReg, data=data_Regret, family = binomial)
LogisticCopeland <- glm(formula = Score ~ RulesCop, data=data_Copeland, family = binomial)
LogisticGini <- glm(formula = Score ~ RulesGini, data=data_Gini, family = binomial)
LogisticNew <- glm(formula = Score ~ RulesNew, data=data_New, family = binomial)

##Posthoc analysis
posthocLogComm <- summary(glht(LogisticCommittee, mcp(RulesComm="Tukey")))
posthocLogMinority <- summary(glht(LogisticMinority, mcp(RulesMin="Tukey")))
posthocLogRegret <- summary(glht(LogisticRegret, mcp(RulesReg="Tukey")))
posthocLogCop <- summary(glht(LogisticCopeland, mcp(RulesCop="Tukey")))
posthocLogGini <- summary(glht(LogisticGini, mcp(RulesGini="Tukey")))
posthocLogNew <- summary(glht(LogisticNew, mcp(RulesNew="Tukey")))