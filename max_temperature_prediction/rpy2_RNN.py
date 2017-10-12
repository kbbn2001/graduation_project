from rpy2.robjects.packages import importr
import rpy2.robjects as robjects
import datetime as dt
from bgfunc import dirCheck

def RNN_learn(train_data_path,test_data_path,epochs,hidden_dim):
	start_time = dt.datetime.now()

	result_name = "result"


	models_path = "./models/1.rda"
	dirCheck(models_path)
	models_path = "\"./\""


	
	importr("rnn")
	robjects.r('''   
	memory.limit(size = 14000)
	loop_size = 10
	setwd(''' + models_path + ''')
	train_epochs = '''+epochs+'''
	train_learningRate = 0.1
	train_dim = '''+hidden_dim+'''
	
	int2bin <- function(integer, length=8) {
	  t(sapply(integer, i2b, length=length))
	}
	
	
	i2b <- function(integer, length=8){
	  as.numeric(intToBits(integer))[1:length]
	}
	
	bin2int <- function(binary){
	  
	  # round
	  binary <- round(binary)
	  
	  # determine length of binary representation
	  length <- dim(binary)[2]
	  
	  # apply to full matrix
	  apply(binary, 1, b2i)
	}
	
	b2i <- function(binary){
	packBits(as.raw(c(binary, rep(0, 32-length(binary) ))), 'integer')
	}
	
	# 학습데이터 로드 
	data <- read.csv(\"''' + train_data_path + '''\" , header = FALSE)
	train_data <- data[,1:ncol(data) - 1]
	train_label <- data[,ncol(data)]
	a1 <- int2bin(train_data[,1])
	a2 <- int2bin(train_data[,2])
	rnn_train_data <- array(c(a1, a2) , dim= c(dim(a1),2))
	for ( i in 3:ncol(train_data))
	{
		temp <- int2bin(train_data[,i])
		rnn_train_data <- array(c(rnn_train_data, temp), dim=c(dim(rnn_train_data)[1] , dim(rnn_train_data)[2] ,  dim(rnn_train_data)[3] + 1))
	}
	
	rnn_train_label <- int2bin(train_label)
	
	# 테스트 데이터 로드 
	data <- read.csv(\"''' + test_data_path + '''\" , header = FALSE)
	
	test_data <- data[,1:ncol(data) - 1]
	test_label <- data[,ncol(data)]
	
	a1 <- int2bin(test_data[,1])
	a2 <- int2bin(test_data[,2])
	
	rnn_test_data <- array(c(a1, a2) , dim= c(dim(a1),2))
	
	for ( i in 3:ncol(test_data))
	{
		temp <- int2bin(test_data[,i])
		rnn_test_data <- array(c(rnn_test_data, temp), dim=c(dim(rnn_test_data)[1] , dim(rnn_test_data)[2] ,  dim(rnn_test_data)[3] + 1))
	}
	
	my_predictions = c()
	
	model <- trainr(Y=rnn_train_label[,dim(rnn_train_label)[2]:1],
		X=rnn_train_data[,dim(rnn_train_data)[2]:1,],
		network_type = "rnn",
		use_bias = T,
		numepochs = train_epochs,
		learningrate   =  train_learningRate,
		hidden_dim     = train_dim
		)
	
		predictions <- predictr(model, rnn_test_data[,dim(rnn_test_data)[2]:1,])
		predictions = predictions[,dim(predictions)[2]:1]
		predictions <- bin2int(predictions)
		
			
		filePath = paste("./models/model.rda", sep="")
		save( model, file = filePath )
	
	''')
	test_label = robjects.r('test_label')
	prediction = robjects.r('predictions')

	end_time = dt.datetime.now()

	time_stamp_file = open('./graph/' + result_name + '_RNN_time.txt', 'w')
	time_stamp_file.write("result = ")
	time_stamp_file.write(str(prediction))
	time_stamp_file.write("\n")
	time_stamp_file.write("running time = ")
	time_stamp_file.write(str(end_time - start_time))
	time_stamp_file.write("\n")
	time_stamp_file.close()

	print(end_time - start_time)
	print(dt.datetime.now())

	return prediction,test_label
