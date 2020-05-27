# Twitter-Sentiment-Analysis-for-COVID-19-tweets

This project is particularly a sentiment analysis of the COVID-19 tweets that has been tweeted in the past couple of months. Sentiment Analysis refers to Natural Language Processing to determine the attitude , opinion or in a more technical term to determine the Polarity of the tweet. Sentiment of tweet can be either Positive or Negative depending on the Tweet score.

For this project I have used a sample data set of almost 10 lakh tweets from IEEE dataport, refined it and prepared a training data set.

For creating a Sentiment Analysis using Twitter we need to apply for Twitter developer API and request for API key. (In the code I have hardcoded the API key for security purposes)

For language pre-processing and cleaning I have used NLTK Library available under Python Language. For classification I have used Naive Bayes Classifier

Naive Bayes Classifier is a classification algorithm that relies on Bayes’ Theorem. This theorem provides a way of calculating a type or probability called posterior probability, in which the probability of an event A occurring is reliant on probabilistic known background (e.g. event B evidence).

The code is divided under 5 major sections:

(1) Preparing the Test Set
		(1.a) Getting Authentication Credentials from Twitter
		(1.b) Authenticating the credentials
		(1.c) Function to build a test set
		
(2) Preparing the Training Set

(3) Pre-processing the tweets in the Data set -  Stemming, Lemmatization, Stopword removal

(4) Naive-Bayes Classifier
		(4.a) Matching tweets against our Vocabulary
		(4.b) Building the feature vector
		(4.c) Training our Classifier
		
(5) Testing the model against Training data set
