#API Call Examples:
#https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=37.5485&lon=-121.988571&dt=1612569600&appid=0bb2c8b8f51f03a3b08d013632ecfc7a
#https://api.openweathermap.org/data/2.5/onecall?lat=37.5485&lon=-121.988571&appid=0bb2c8b8f51f03a3b08d013632ecfc7a
import CYKParse
import Tree
import Weatherfunc

if __name__ == "__main__":
    toTerminate = False
    print("Hello, I am Raja and will answer your questions about the weather.\nType 'Thank You' to end the conversation.")
    print("Please ensure your request or message ends with punctuation.\n")
    while (toTerminate == False):
        print("")
        sentence = input()
        
        if (sentence.lower() == "thank you" or sentence.lower()[:-1] == "thank you"):
            toTerminate = True
            break

        sentence = (sentence.strip())[:-1] #remove punctuation and surrounding punctuation
        backup_sentence = sentence
        sentence = sentence[0].lower() + sentence[1:] #make first letter lowercase

        T,P = CYKParse.CYKParse(sentence.split(), CYKParse.getGrammarWeatherCustomLocations(Proj1.locations))
        sentenceTree = Proj1.getSentenceParse(T)

        if (sentenceTree != ''):
            Proj1.updateRequestInfo(sentenceTree)
            Proj1.reply()

        else:
            T,P = CYKParse.CYKParse(backup_sentence.split(), CYKParse.getGrammarWeatherCustomLocations(Proj1.locations))
            sentenceTree = Proj1.getSentenceParse(T)

            if (sentenceTree != ''):
                Proj1.updateRequestInfo(sentenceTree)
                Proj1.reply()
            else:
                print('You have not requested a sentence that I can understand, since I am not that intelligent.')


