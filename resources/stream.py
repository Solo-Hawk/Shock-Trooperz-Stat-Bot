import discord
import censusapi
import time
import asyncio
token = 'MjY2NzU3OTE4ODU3MjMyMzg0.C1UDeQ.iEP6hp4KukY7bev8j9q6LlB6OwU'
apikey = "558296"
prefix = '!!'
stream_channel_id = '286864838720880640'
fault = 'fault'
update = 120
client = discord.Client()

if __name__ == "__main__":

    @client.event
    async def on_ready():
        clock = update
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
        server = client.get_server('266346794785439745')
        stream_channel = server.get_channel(stream_channel_id)
        print(stream_channel)
        print(server.roles[3])
        territory = censusapi.get_json2("http://ps2.fisu.pw/api/territory/?world=17&continent=0")
        population = censusapi.get_json2("http://ps2.fisu.pw/api/population/?world=17")
        censusapi.style_stream_data(territory, population)





        timer = await client.send_message(stream_channel, str(clock) + ' Seconds until update')
        message = await client.send_message(stream_channel,'Loading API...')

        # TR = 3
        while True:
            for x in range(update):
                time.sleep(1)
                clock -= 1
                if clock < 10:
                    await client.edit_message(timer, '0' + str(clock) + ' Seconds until update')
                else:
                    await client.edit_message(timer, str(clock) + ' Seconds until update')

            territory = censusapi.get_json2("http://ps2.fisu.pw/api/territory/?world=17&continent=0")
            population = censusapi.get_json2("http://ps2.fisu.pw/api/population/?world=17")
            try:
                response = censusapi.style_stream_data(territory, population, members)

                await client.edit_message(message, response)
            except IndexError:
                print(fault)
            clock = update
            await client.edit_message(timer, str(clock) + ' Seconds until update')
    client.run(token)
