# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import traceback
from datetime import datetime
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    TurnContext,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from botbuilder.schema import Activity, ActivityTypes

from bots import EchoBot
from config import DefaultConfig

import google.generativeai as palm

CONFIG = DefaultConfig()

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))


# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)


ADAPTER.on_turn_error = on_error

# Create the Bot
BOT = EchoBot()


# Listen for incoming requests on /api/messages
# async def messages(req: Request) -> Response:
#     return await ADAPTER.process(req, BOT)


# Listen for incoming requests on /api/messages and reverse the message
async def messages(req: Request) -> Response:

    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()

        print(body)

        # models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
        # model = models[0].name

        model = "models/text-bison-001"

        ## Reverse string entered by user
        # print("Original string = ", body)
        # body["text"] = body["text"][::-1]
        # print("Reversed string = ", body)

        ## Check if the string entered by user is a palindrome
        # if body["text"] == body["text"][::-1]:
        #     print(body["text"], "is a palindrome")
        #     body["text"] = body["text"] + " is a palindrome"
            
        # else:
        #     print(body["text"], "is not a palindrome")
        #     body["text"] = body["text"] + " is not a palindrome"

        ## Asking PALM user asked questions

        # body["text"] = palm.chat(messages = "how are you?")

        print("key --------------------", CONFIG.API_KEY)

        palm.configure(api_key = f'{CONFIG.API_KEY}') 

        completion = palm.generate_text(
            model=model,
            prompt=body["text"],
            temperature=0,
            # The maximum length of the response
            max_output_tokens=800,
        )

        print(completion.result)

        body["text"] = completion.result
    
    else:
        return Response(status = HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    
    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(auth_header, activity, BOT.on_turn)

    if response:
        return json_response(data = response.body, status = response.status)
    
    return Response(status = HTTPStatus.OK)


APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
