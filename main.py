from scrapers import *
from settings import BOT_TOKEN
import discord

#Globals

client = discord.Client()
searchTerm = ""
location = "Toronto"
timeSpan = "3"

def displayListings(resultList:list)-> str:
    #remove counter to allow more outputs
    output = ""
    for JOB in resultList:
        result = getTemplate().format(
            JOB.jobTitle,
            JOB.jobCompany,
            JOB.jobLink
        )
        output+=result
    return output

def getTemplate()->str:            
    outputTemplate = "**Position**: {}\n**Company**: {}\n**Link**: {}\n\n"
    return outputTemplate

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

            embed = discord.Embed(
                title = "Jobs Found for Search -> '{}'".format(searchTerm),
                colour = discord.Colour.orange()  
            )
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)

            amount_of_entries = 0
            for JOB in webScrapeResults:

                embed.add_field(name='Position',value=JOB.jobTitle, inline=True)
                embed.add_field(name='Company',value=JOB.jobCompany, inline=True)
                embed.add_field(name='Link',value='[Here]({})'.format(JOB.jobLink), inline=True)
                amount_of_entries +=1

                if (amount_of_entries > 8 and len(webScrapeResults) > 8):
                    #send above embed
                    await message.channel.send(embed=embed)
                    embed = discord.Embed(
                    colour = discord.Colour.orange()  
                    )

                    for i in range(9,len(webScrapeResults)):
                        embed.add_field(name='Position',value=webScrapeResults[i].jobTitle, inline=True)
                        embed.add_field(name='Company',value=webScrapeResults[i].jobCompany, inline=True)
                        embed.add_field(name='Link',value='[Here]({})'.format(webScrapeResults[i].jobLink), inline=True)
                    break

            await message.channel.send(embed=embed)

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
    
client.run(BOT_TOKEN)

#TESTfd
#def main():
#    scrapeForMe = scrapeIndeed("associate","toronto","3")
#    foundPositions = scrapeForMe.collectPostings()
#    print(displayListings(foundPositions))
#if __name__ == '__main__':
#    main()