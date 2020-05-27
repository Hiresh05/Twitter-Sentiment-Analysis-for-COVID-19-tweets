import twitter
import time 
import csv
import re
import nltk
from nltk.tokenize import word_tokenize
from string import punctuation 
from nltk.corpus import stopwords
           
twitter_api = twitter.Api(consumer_key='407J0LY1RDuzg####IMAiEWpj',
                        consumer_secret='qlBPH1rlATqt7jyLk2pfCYEsy1kClCurTtfaX####HalJwemH4',
                        access_token_key='2503735328####le3qAUUQe6KCQzvxEbetNBoxAXurN8L8TYp',
                        access_token_secret='yvIaE1ygqczvUsDD7XLgXBBne####yY8p7MrvQENyDQgW')

print(twitter_api.VerifyCredentials())
 

#now we have verified our credentials , lets search for tweets from dataset
# I have downloaded sample tweets data set from IEEE data port consisiting of more than 10 lakhs tweeet

def buildTestSet(search_keyword):
    try:
        tweets_fetched = twitter_api.GetSearch(search_keyword, count = 100)
        
        print("Fetched " + str(len(tweets_fetched)) + " tweets for the term " + search_keyword)
        
        return [{"text":status.text, "label":None} for status in tweets_fetched]
    except:
        print("Can't fetch the tweet , something went wrong ....")
        return None

# Returns first 5 tweets containing the keyword
search_term = input("Enter a search keyword:")
testDataSet = buildTestSet(search_term)

print(testDataSet[0:4])


#Only 180 requests can be processed at one time. Creating a training data set and iterating it through the last

def buidTrainingSet(corpusFile, tweetDataFile):
    
    corpus = []
    
    with open(corpusFile,'rb') as csvfile:
        lineReader = csv.reader(csvfile,delimiter=',', quotechar="\"")
        for row in lineReader:
            corpus.append({"tweet_id":row[2], "label":row[1], "topic":row[0]})
            
    rate_limit = 180
    sleep_time = 900/180
    
    trainingDataSet = []
    
    for tweet in corpus:
        try:
            status = twitter_api.GetStatus(tweet["tweet_id"])
            print("Tweet fetched" + status.text)
            tweet["text"] = status.text
            trainingDataSet.append(tweet)
            time.sleep(sleep_time) 
        except: 
            continue

    with open(tweetDataFile,'wb') as csvfile:
        linewriter = csv.writer(csvfile,delimiter=',',quotechar="\"")
        for tweet in trainingDataSet:
            try:
                linewriter.writerow([tweet["tweet_id"], tweet["text"], tweet["label"], tweet["topic"]])
            except Exception as e:
                print(e)
    return trainingDataSet

corpusFile = "YOUR_FILE_PATH/corpus.csv"
tweetDataFile = "YOUR_FILE_PATH/tweetDataFile.csv"

trainingData = buildTrainingSet(corpusFile, tweetDataFile)

#Now we have read the tweets. Lets clean the tweet and make it in readable format

    def __init__(self):
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER','URL'])
        
    def processTweets(self, list_of_tweets):
        processedTweets=[]
        for tweet in list_of_tweets:
            processedTweets.append((self._processTweet(tweet["text"]),tweet["label"]))
        return processedTweets
    
    def _processTweet(self, tweet):
        tweet = tweet.lower() # convert text to lowercase for consistency
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet) # remove URLs
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet) # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet) # remove the # in #hashtag
        tweet = word_tokenize(tweet) # remove repeated characters 
        return [word for word in tweet if word not in self._stopwords]

tweetProcessor = PreProcessTweets()
preprocessedTrainingSet = tweetProcessor.processTweets(trainingData)
preprocessedTestSet = tweetProcessor.processTweets(testDataSet)

def buildVocabulary(preprocessedTrainingData):
    all_words = []
    
    for (words, sentiment) in preprocessedTrainingData:
        all_words.extend(words)

    wordlist = nltk.FreqDist(all_words)
    word_features = wordlist.keys()
    
    return word_features

def extract_features(tweet):
    tweet_words=set(tweet)
    features={}
    for word in word_features:
        features['contains(%s)' % word]=(word in tweet_words)
    return features

word_features = buildVocabulary(preprocessedTrainingSet)
trainingFeatures=nltk.classify.apply_features(extract_features,preprocessedTrainingSet)

NBayesClassifier=nltk.NaiveBayesClassifier.train(trainingFeatures)

NBResultLabels = [NBayesClassifier.classify(extract_features(tweet[0])) for tweet in preprocessedTestSet]

if NBResultLabels.count('pos') > NBResultLabels.count('neg'):
    print("Overall Positive Sentiment")
    print("Positive Sentiment Percentage = " + str(100*NBResultLabels.count('pos')/len(NBResultLabels)) + "%")
else: 
    print("Overall Negative Sentiment")
    print("Negative Sentiment Percentage = " + str(100*NBResultLabels.count('neg')/len(NBResultLabels)) + "%")
