library(tseries)

Lags <- vector(mode="numeric", length=0)
Correlations <- vector(mode="numeric", length=0)
Lags_nonStat <- vector(mode="numeric", length=0)
Correlations_nonStat <- vector(mode="numeric", length=0)

Find_Max_CCF<- function(a,b)
{
 d <- ccf(a, b, plot = FALSE)
 cor = d$acf[,,1]
 lag = d$lag[,,1]
 res = data.frame(cor,lag)
 minIndex = which.max(abs(res$cor))
 retVal <- c(res$cor[minIndex], res$lag[minIndex])
 #res_max = res[which.max(abs(res$cor)),]
}

Differencing <- function(x,y)
{
framework_x_seasdiff <- diff(x, differences=1)  # seasonal differencing
framework_x_Stationary <- diff(framework_x_seasdiff, differences= 1)
framework_y_seasdiff <- diff(y, differences=1)  # seasonal differencing
framework_y_Stationary <- diff(framework_y_seasdiff, differences= 1)
return(list(framework_x_Stationary,framework_y_Stationary))
}

# NodeJS
NodeJS_x <- as.ts(c(95,45,85,141,92,89,73,58,127,142,343,150,88,149,115,2,288,124,251,353,129,104,67,49,23,410,360,306,196,239,91,76,284,476,166,342,274,196,347,186,220,15,312,222,178,473,219,193,263,132,303,123,182,119,54,288,44,163,161,28,37,19,355,2,0,707,219,172,155,185,141,273,63,147,291,0,0,0,0,0,1279,0,0,0,0,0,1287,0,0,0,0,0,0,2611,0,0,0)) 
NodeJS_y <- as.ts(c(-0.0194,0.1286,-0.0488,-0.0149,-0.0270,-0.0400,-0.0051,-0.0347,0.0049,0.0217,-0.0239,-0.0197,-0.0344,-0.0345,0.0107,-0.0212,0.0722,-0.0001,-0.0321,-0.0088,-0.0291,0.0010,0.0196,-0.0402,0.0108,-0.0401,-0.0133,-0.0716,0.0025,0.0011,-0.0191,-0.0056,0.0092,0.0299,0.0152,-0.0035,-0.0877,-0.0381,0.0245,-0.0268,-0.0375,-0.0062,-0.0085,-0.0083,-0.0529,0.0027,-0.0108,-0.0274,-0.0370,-0.0285,0.0039,-0.0029,-0.0327,0.0004,-0.0149,0.0008,-0.0655,0.0100,-0.0054,-0.0227,-0.0126,0.0174,0.0027,0.0131,0.0462,0.0487,0.0354,-0.0227,0.0047,0.0315,0.0306,0.0416,0.0805,0.0931,0.0867,0.0413,0.0392,0.0236,0.0757,0.0379,0.0703,0.0564,0.0635,0.0625,0.0126,0.0271,0.0338,-0.0254,0.0342,-0.0061,0.0261,0.0141,0.0258,0.0038,-0.0135,-0.0106,0.0269))
adf.test(NodeJS_x)
ccf(NodeJS_x, NodeJS_y)
print("NodeJS")
cor.test(NodeJS_x,NodeJS_y)
#differencedVals <- Differencing(NodeJS_x, NodeJS_y)
#ccf(differencedVals[1], differencedVals[2])
framework_x_seasdiff <- diff(NodeJS_x, lag=frequency(NodeJS_x), differences=1)  # seasonal differencing
framework_x_Stationary <- diff(framework_x_seasdiff, differences= 1)
framework_y_seasdiff <- diff(NodeJS_y, lag=frequency(NodeJS_y), differences=1)  # seasonal differencing
framework_y_Stationary <- diff(framework_y_seasdiff, differences= 1)
MaxCff <- Find_Max_CCF(framework_x_Stationary, framework_y_Stationary)
Lags <- c(Lags, MaxCff[2])
Correlations <- c(Correlations, MaxCff[1])
MaxCff <- Find_Max_CCF(NodeJS_x, NodeJS_y)
Lags_nonStat <- c(Lags_nonStat, MaxCff[2])
Correlations_nonStat <- c(Correlations_nonStat, MaxCff[1])

# AngularJS
AngularJS_x <- as.ts(c(33,150,31,97,47,78,46,158,90,0,106,105,33,181,240,87,49,69,108,135,87,69,82,179,375,488,255,673,165,183,100,396,113,149,131,241,293,182,296,134,145,121,106,78,96,78,67,53,112,129,112,64,156,32,96,0,0,0,0,571,70,41,0,0,0,0)) 
AngularJS_y <- as.ts(c(-0.1084,-0.1575,0.0292,-0.0992,-0.1156,-0.0186,-0.0341,-0.0745,-0.0352,-0.0366,-0.0296,-0.0683,0.058,-0.0008,-0.042,0.0325,-0.0333,-0.0492,0.0389,0.0192,0.0274,-0.0238,-0.0329,0.0321,0.0091,-0.0289,0.0291,0.0088,0.0048,0.0093,-0.0005,0.0078,0.0133,0.0332,0.0457,0.0001,0.0123,-0.0484,0.0481,0.0273,0.0262,-0.0389,0.0474,0.0551,-0.0273,0.0117,0.0241,0.026,-0.0066,0.0409,0.0295,0.0447,0.0088,0.025,0.0552,0.0292,0.0128,0.0484,0.0555,0.0394,0.0259,0.0434,0.0366,0.0253,0.0635,0.0416))
adf.test(AngularJS_x)
ccf(AngularJS_x, AngularJS_y)
cor.test(AngularJS_x,AngularJS_y)
print("AngularJS")
framework_x_seasdiff <- diff(AngularJS_x, lag=frequency(AngularJS_x), differences=1)  # seasonal differencing
framework_x_Stationary <- diff(framework_x_seasdiff, differences= 1)
framework_y_seasdiff <- diff(AngularJS_y, lag=frequency(AngularJS_y), differences=1)  # seasonal differencing
framework_y_Stationary <- diff(framework_y_seasdiff, differences= 1)
MaxCff <- Find_Max_CCF(framework_x_Stationary, framework_y_Stationary)
Lags <- c(Lags, MaxCff[2])
Correlations <- c(Correlations, MaxCff[1])
MaxCff <- Find_Max_CCF(AngularJS_x, AngularJS_y)
Lags_nonStat <- c(Lags_nonStat, MaxCff[2])
Correlations_nonStat <- c(Correlations_nonStat, MaxCff[1])

# EmberJS
EmberJS_x <- as.ts(c(275,200,65,252,81,192,688,275,447,230,273,187,338,138,5,505,187,275,175,1,362,272,0,256,0,433,494,0,268,459,717,0,858,0,342,0,582,0,0,798,0,372,0,425,157,0,759,0,350,57,718,0,834,99,164,0,209,0,193,180,353,0,294,0)) 
EmberJS_y <- as.ts(c(0.01732322455,-0.01723892112,-0.02681389286,0.00391397193,-0.01774652899,-0.001011804964,-0.04538229526,0.009078971531,-0.0218661185,-0.02548341243,-0.0563962777,-0.01292310454,0.01021914092,-0.01955927329,-0.04667182408,-0.03147949705,-0.01437176001,-0.04755444194,0.01757376605,0.0105670655,-0.004028248821,-0.1266480057,0.03581382664,-0.06106104969,0.01082189707,0.009365853415,0.04111861294,0.02618932617,0.02774719052,-0.04415177074,-0.02197808939,-0.08962977427,0.05469722804,-0.0238470829,-0.0289646396,0.003792518405,0.01041952844,0.0251329165,-0.004535868203,0.06821042167,-0.01062082899,0.03516522499,-0.01534194182,0.07905043671,-0.03480634497,0.02364247242,0.03673181314,0.04039331481,0.02819265681,0.07766346369,0.05099052303,-0.01790983617,0.0259178167,-0.004606733329,0.04800252773,0.03786052563,0.0855099058,0.04651536604,0.00737657021,0.056172864,0.03538680274,0.006574519793,0.02377909681,0.02096210939))
adf.test(EmberJS_x)
res <- ccf(EmberJS_x, EmberJS_y)
cor.test(EmberJS_x, EmberJS_y)
print("EmberJS")
framework_x_seasdiff <- diff(EmberJS_x, lag=frequency(EmberJS_x), differences=1)  # seasonal differencing
framework_x_Stationary <- diff(framework_x_seasdiff, differences= 1)
framework_y_seasdiff <- diff(EmberJS_y, lag=frequency(EmberJS_y), differences=1)  # seasonal differencing
framework_y_Stationary <- diff(framework_y_seasdiff, differences= 1)
MaxCff <- Find_Max_CCF(framework_x_Stationary, framework_y_Stationary)
Lags <- c(Lags, MaxCff[2])
Correlations <- c(Correlations, MaxCff[1])
MaxCff <- Find_Max_CCF(EmberJS_x, EmberJS_y)
Lags_nonStat <- c(Lags_nonStat, MaxCff[2])
Correlations_nonStat <- c(Correlations_nonStat, MaxCff[1])

# VueJS
VueJS_x <- as.ts(c(0,0,0,0,309,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,768,146,145,95,53,158,140,50,144,87,126,34,0,164,87,103,33)) 
VueJS_y <- as.ts(c(0.1172559828,-0.03555337148,-0.1268334595,-0.03373730986,-0.0506633419,0.006292270645,-0.01819765592,0.0428143005,0.05372391472,0.02641730392,0.03724630427,-0.04476878026,0.05278399782,-0.04645256367,0.02484665356,-0.04773947791,0.01645917059,-0.05000134714,-0.008792550042,-0.02335340305,-0.002125524179,0.02902115283,0.00660235092,0.04931546856,0.01660418708,0.04014299728,0.007633961892,0.0389045521,0.04184307012,-0.001110180199,-0.01966949393,0.01633896897,0.05900793982,0.04280209775,0.03115835861,-0.03255466587,0.03891641911,-0.002104625205,0.02489340194,0.004944847555,0.02106256612,0.02106256612))
adf.test(VueJS_x)
cor.test(VueJS_x, VueJS_y)
ccf(VueJS_x, VueJS_y)
print("VueJS")
framework_x_seasdiff <- diff(VueJS_x, lag=frequency(VueJS_x), differences=1)  # seasonal differencing
framework_x_Stationary <- diff(framework_x_seasdiff, differences= 1)
framework_y_seasdiff <- diff(VueJS_y, lag=frequency(VueJS_y), differences=1)  # seasonal differencing
framework_y_Stationary <- diff(framework_y_seasdiff, differences= 1)
MaxCff <- Find_Max_CCF(framework_x_Stationary, framework_y_Stationary)
Lags <- c(Lags, MaxCff[2])
Correlations <- c(Correlations, MaxCff[1])
MaxCff <- Find_Max_CCF(VueJS_x, VueJS_y)
Lags_nonStat <- c(Lags_nonStat, MaxCff[2])
Correlations_nonStat <- c(Correlations_nonStat, MaxCff[1])

# CakePhp
CakePhp_x <- as.ts(c(0,41,115,44,2028,897,1684,621,79,17,56,0,80,59,30,1832,62,49,3076,480,3701,778,177,133,436,661,468,454,533,133,471,116,453,683,609,2,92,136,51,94,410,795,81,158,104,63,2964,1678,618,1541,5450,606,572,935,257,1044,262,8073,428,4927,234,317,247,124,1033,415,219,139,132,711,200,259,106,155,151,686,673,223,95,110,539,1202,671,155,14,125,180,768,1069,117,75)) 
CakePhp_y <- as.ts(c(-0.05580574615,-0.06525433368,-0.03891643084,-0.04270666342,0.0169190524,0.02539155,0.01789571335,-0.02361095807,0.00114438607,-0.02638691169,0.05404891577,0.009806658209,-0.001332428641,-0.004093764304,0.004157034916,-0.01423893165,-0.02274757827,0.001242529538,0.02248699686,-0.004841808593,-0.0134458891,0.03151609773,0.00452547936,-0.04932091654,0.04961371319,0.006646836216,-0.0249841699,0.003737606301,0.04532763925,-0.008486330937,0.05830528025,-0.01442533413,0.01222650577,0.0599344542,-0.0202853544,0.02256439216,-0.01217549762,0.01593261022,0.005254874381,0.03916959489,0.003906803564,-0.01162236977,-0.005484847673,0.01874974094,0.03307246094,0.01018062603,-0.03461889763,0.03270454336,-0.01461331643,0.002324400768,0.005313689687,0.007447227706,-0.01426143459,-0.0233384385,0.01480319514,0.008386356787,-0.0197576351,0.04059122306,0.01677971955,-0.005622980443,-0.002851295004,-0.007148385111,0.001765620931,-0.02467958478,-0.01403696081,-0.008504790608,-0.009498430341,-0.05419570114,-0.02837045074,-0.008646898259,-0.04242954879,-0.00743371178,-0.005628539716,0.01112563378,0.01804333256,-0.0002050029523,-0.02018188965,0.002584957551,0.006289240641,0.01226832971,0.04809863671,0.00344194721,0.01663404008,0.008210777916,0.03753361519,0.05827261507,0.04344402917,-0.0417118585,0.02815573507,0.02870466679,0.009630015704))
adf.test(CakePhp_x)
ccf(CakePhp_x, CakePhp_y)
print("CakePhp")
cor.test(CakePhp_x, CakePhp_y)
framework_x_seasdiff <- diff(CakePhp_x, lag=frequency(CakePhp_x), differences=1)  # seasonal differencing
framework_x_Stationary <- diff(framework_x_seasdiff, differences= 1)
framework_y_seasdiff <- diff(CakePhp_y, lag=frequency(CakePhp_y), differences=1)  # seasonal differencing
framework_y_Stationary <- diff(framework_y_seasdiff, differences= 1)
MaxCff <- Find_Max_CCF(framework_x_Stationary, framework_y_Stationary)
Lags <- c(Lags, MaxCff[2])
Correlations <- c(Correlations, MaxCff[1])
MaxCff <- Find_Max_CCF(CakePhp_x, CakePhp_y)
Lags_nonStat <- c(Lags_nonStat, MaxCff[2])
Correlations_nonStat <- c(Correlations_nonStat, MaxCff[1])

# Laravel
Laravel_x <- as.ts(c(0,275,256,25,436,56,350,145,61,19,192,18,64,188,15,3,6,5,99,7,33,48,18,413,44,154,8,33,65,27,54,66,244,33,5,146,22,33,56,10,20,84,54,25,72,11))
Laravel_y <- as.ts(c(0.05957741842,0.04160998777,0.0261462484,0.02707601536,0.004707656637,0.04800663999,-0.003925299603,0.03778651314,0.03135891303,0.04530210005,0.03425446808,-0.0004293549005,0.03205605468,0.01013209144,-0.03542623075,-0.01872885801,0.02851837425,-0.02451623153,-0.02867318399,-0.006130322802,-0.02441709733,-0.04005017101,0.006239752663,0.004897549112,-0.003985703987,-0.0002354004809,0.01426196306,-0.01216092007,-0.02197273297,-0.01285678068,-0.03048780696,-0.01211982487,0.01320774154,0.02541968025,-0.002792136027,-0.02172099326,-0.003107515261,-0.02778698021,-0.01862156393,0.01066093272,-0.03846072692,-0.01511989506,-0.02107776113,-0.02107776113,-0.02107776113,-0.02107776113))
adf.test(Laravel_x)
ccf(Laravel_x, Laravel_y)
print("Laravel")
cor.test(Laravel_x, Laravel_y)
framework_x_seasdiff <- diff(Laravel_x, lag=frequency(Laravel_x), differences=1)  # seasonal differencing
framework_x_Stationary <- diff(framework_x_seasdiff, differences= 1)
framework_y_seasdiff <- diff(Laravel_y, lag=frequency(Laravel_y), differences=1)  # seasonal differencing
framework_y_Stationary <- diff(framework_y_seasdiff, differences= 1)
MaxCff <- Find_Max_CCF(framework_x_Stationary, framework_y_Stationary)
Lags <- c(Lags, MaxCff[2])
Correlations <- c(Correlations, MaxCff[1])
MaxCff <- Find_Max_CCF(Laravel_x, Laravel_y)
Lags_nonStat <- c(Lags_nonStat, MaxCff[2])
Correlations_nonStat <- c(Correlations_nonStat, MaxCff[1])


# Symfony
Symfony_x <- as.ts(c(0,399,357,361,1300,1029,722,676,558,128,119,420,49,103,62,119,87,39,65,3590,221,184,183,188,91,1520,224,112,1153,152,395,375,709,326,277,337,336,1158,492,486,142,1034,132,825,140,961,269,417,1012,878,106,642,506,456,3047,885,370,1838,1023,261,1209,1169,509,523,1377,690,581,929,468,617,464,2149,188,931,597,82,708,1325,609,1174,103,610,817,843))
Symfony_y <- as.ts(c(-0.02888071008,-0.007038286834,-0.04124227609,-0.01448135131,0.03188375323,0.02088561182,0.04402973707,0.02920367002,0.006201923238,-0.003799295658,-0.01620846789,-0.006465984467,-0.003928134376,-0.02844665337,0.02829928754,0.02498932639,-0.058403876,0.02998952741,0.04285808073,0.01086908127,0.05007039181,0.04032129574,0.009222612298,-0.04166763415,-0.05041764029,-0.03279973255,0.05349793226,-0.0213347779,0.0397383843,-0.02427785575,-0.07728469839,0.01610874801,0.007960628565,0.05418344904,0.02417317988,-0.04396987382,0.03266273805,0.001734593201,-0.03760951424,0.03970765374,-0.07415881449,0.03751150256,0.02881520676,-0.03519093544,0.004881825068,-0.08965694526,0.04243506055,0.06302793535,0.02455562359,-0.02765445331,-0.0156779922,-0.004245036028,0.01271946919,0.009193437154,0.06764851685,0.02038222693,0.02383025992,0.03873505426,0.003808318876,-0.00899469472,-0.01228333126,-0.02878877418,-0.004614612067,0.01283455283,0.0113323214,0.02130768673,0.002365195097,-0.03662101456,-0.005586037928,0.001695470596,0.04048806214,-0.03087368601,0.01371016168,-0.04945713858,0.009907046335,-0.04382569704,-0.1187127129,0.03635877276,0.01866082462,0.03045322591,0.04704464942,0.0177748524,0.02530665671,0.02530665671))
adf.test(Symfony_x)
ccf(Symfony_x, Symfony_y)
print("Symfony")
cor.test(Symfony_x, Symfony_y)
framework_x_seasdiff <- diff(Symfony_x, lag=frequency(Symfony_x), differences=1)  # seasonal differencing
framework_x_Stationary <- diff(framework_x_seasdiff, differences= 1)
framework_y_seasdiff <- diff(Symfony_y, lag=frequency(Symfony_y), differences=1)  # seasonal differencing
framework_y_Stationary <- diff(framework_y_seasdiff, differences= 1)
MaxCff <- Find_Max_CCF(framework_x_Stationary, framework_y_Stationary)
Lags <- c(Lags, MaxCff[2])
Correlations <- c(Correlations, MaxCff[1])
MaxCff <- Find_Max_CCF(Symfony_x, Symfony_y)
Lags_nonStat <- c(Lags_nonStat, MaxCff[2])
Correlations_nonStat <- c(Correlations_nonStat, MaxCff[1])

# FINAL PLOT
plot(Lags, Correlations, main="Highest correlation for every OSS project", pch=c(15), col = c("brown","red", "green","blue", "orange", "purple", "black"), cex=1.5, ylim=c(-0.6,0.6), xlim=c(-15,20))
grid(nx=20,ny=30)
legend(-15,0.6, legend=c("NodeJS", "AngularJS","EmberJS","VueJS","CakePHP","Laravel","Symfony"),col=c("brown","red", "green","blue", "orange", "purple", "black"), cex=1.2,  pch = c(15))

# FINAL PLOT NONSTAT
plot(Lags_nonStat, Correlations_nonStat, main="Highest correlation for every OSS project", pch=c(15), col = c("brown","red", "green","blue", "orange", "purple", "black"), cex=1.5,ylim=c(-0.6,0.6), xlim=c(-15,20))
grid(nx=20,ny=30)
legend(11,0.6, legend=c("NodeJS", "AngularJS","EmberJS","VueJS","CakePHP","Laravel","Symfony"),col=c("brown","red", "green","blue", "orange", "purple", "black"), cex=1.2,  pch = c(15))


tsdata <- ts(Symfony_y)
adfres <- adf.test(tsdata)
adfres

# Seasonal Differencing
#> 1
framework_y_seasdiff <- diff(NodeJS_y, lag=frequency(NodeJS_y), differences=1)  # seasonal differencing
#plot(framework_y_seasdiff, type="l", main="Seasonally Differenced")  # still not stationary!

# Make it stationary
framework_y_StationaryTS <- diff(framework_y_seasdiff, differences= 1)
#plot(framework_y_StationaryTS, type="l", main="Differenced and Stationary")  # appears to be stationary


#some plots for thesis text
plot.ts(NodeJS_y)
plot.ts(framework_y_StationaryTS)
adf.test(framework_y_StationaryTS)