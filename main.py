from scrapers import *
import discord

#Globals
botTOKEN = "ODY3MTM3MDEyNjAzMjg5NjMx.YPcuRg.BzJdTv22RVkV3rFzsh1ojMbBG-U"

searchTerm = ""
location = "Toronto"
timeSpan = "3"

def displayListings(resultList:list)-> str:
    #remove counter to allow more outputs
    output = ""
    count = 0
    for JOB in resultList:
        result = getTemplate().format(
            JOB.jobTitle,
            JOB.jobCompany,
            JOB.jobLink
        )
        count+=1
        output+=result
        if count >=3:
            break
    return output

def getTemplate()->str:        
    #outputTemplate = """
    #**Position**: {}
    #**Company**: {}
    #**Link**: {}
    #"""    
    outputTemplate = "**Position**: {}\n**Company**: {}\n**Link**: {}\n\n"
    return outputTemplate

def splitMessage(msg)->tuple:
    pass

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):

    #Defaults
    global searchTerm 
    global location
    global timeSpan 

    if message.author == client.user:
        return

    #fetch results with 'searchTerm'
    elif message.content.startswith("&fetch"):
        searchTerm = message.content
        searchTerm = searchTerm[7:]
        if (searchTerm == ""):
            await message.channel.send("Err: Enter a search term!")
        else:
            webScrapeResults = scrapeIndeed(searchTerm, location, timeSpan).collectPostings()
            await message.channel.send(displayListings(webScrapeResults))
    
    #set default location to search with
    elif message.content.startswith("&location"):
        location = message.content
        location = location[10:]
        await message.channel.send("Location has been set to: "+location)

    #set default timespan to search with 
    elif message.content.startswith("&timespan"):
        temp = timeSpan #hold prev value in case input error
        timeSpan = message.content
        str(timeSpan)
        timeSpan = timeSpan[10:]
        if timeSpan=="1" or timeSpan=="3" or timeSpan=="7" or timeSpan=="14":
            await message.channel.send("Time-Span has been set to: "+timeSpan)
        else:
            await message.channel.send("Enter an appriorate time span. Refer to &help!")
            timeSpan = temp
    
    elif message.content.startswith("&help"):
        await message.channel.send("You've accessed the empty help menu.. Too Be Implemented!")

    elif message.content.startswith("&query"):
        await message.channel.send("Location: "+location+" | TimeSpan: "+timeSpan)
    
client.run(botTOKEN)

#TESTfd
#def main():
#    scrapeForMe = scrapeIndeed("associate","toronto","3")
#    foundPositions = scrapeForMe.collectPostings()
#    print(displayListings(foundPositions))
#if __name__ == '__main__':
#    main()