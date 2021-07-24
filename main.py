from os import name
from scrapers import *
from settings import BOT_TOKEN
import discord

#Globals
#Defaults set to Toronto & 3 Day search, with blank search_term

client = discord.Client()
search_term = ""
location = "Toronto"
time_span = "3"

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):

    #Defaults
    global search_term 
    global location
    global time_span 

    if message.author == client.user:
        return

    #fetch results with 'search_term'
    elif message.content.startswith(">fetch"):
        search_term = message.content
        search_term = search_term[7:]
        if (search_term == ""):
            await message.channel.send("Err: Enter a search term!")
        else:
            scrape_results = ScrapeIndeed(search_term, location, time_span).collect_postings()

            embed = discord.Embed(
                title = "Jobs Found for Search -> '{}'".format(search_term),
                colour = discord.Colour.orange()  
            )
            embed.set_author(name = message.author, icon_url = message.author.avatar_url)

            amount_of_entries = 0
            for JOB in scrape_results:
                embed.add_field(name='Position',value=JOB.job_title, inline=True)
                embed.add_field(name='Company',value=JOB.job_company, inline=True)
                embed.add_field(name='Link',value='[Here]({})'.format(JOB.job_link), inline=True)
                amount_of_entries += 1

                if (amount_of_entries > 7 and len(scrape_results) > 8):
                    #send above embed
                    await message.channel.send(embed=embed)
                    embed = discord.Embed(
                    colour = discord.Colour.orange()  
                    )

                    for i in range(9,len(scrape_results)):
                        embed.add_field(name='Position',value=scrape_results[i].job_title, inline=True)
                        embed.add_field(name='Company',value=scrape_results[i].job_company, inline=True)
                        embed.add_field(name='Link',value='[Here]({})'.format(scrape_results[i].job_link), inline=True)
                    break

            await message.channel.send(embed=embed)

    #set default location to search with
    elif message.content.startswith(">location"):
        location = message.content
        location = location[10:]
        await message.channel.send("Location has been set to: "+location)

    #set default time_span to search with 
    elif message.content.startswith(">timespan"):
        temp = time_span #hold prev value in case input error
        time_span = message.content
        str(time_span)
        time_span = time_span[10:]
        if time_span == "1" or time_span == "3" or time_span == "7" or time_span == "14":
            await message.channel.send("TimeSpan has been set to: "+time_span)
        else:
            await message.channel.send("Enter an appriorate time span. Refer to &help!")
            time_span = temp
    
    elif message.content.startswith(">help"):
        embed = discord.Embed(
                title = "Useful Commands",
                colour = discord.Colour.purple(),  
            )
        embed.add_field(name='>fetch',value="input key-word/term used for searching. Returns list of results Ex *>fetch developer*", inline=False)
        embed.add_field(name='>location',value="set location for >fetch command. Ex *>location Toronto*", inline=False)
        embed.add_field(name='>time_span',value="set timespan for >fetch command. Options: '1' (24 hours), '3' days, '7' week, '14' two-week. Ex *>time_span 3*", inline=False)
        embed.add_field(name='>query',value="returns current location and time_span settings. Ex *>query*", inline=False)
        await message.channel.send(embed=embed)

    elif message.content.startswith(">query"):
        await message.channel.send("Location: "+location+" | time_span: "+time_span)
        
client.run(BOT_TOKEN)
