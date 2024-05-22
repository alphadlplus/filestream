# Taken from megadlbot_oss <https://github.com/eyaadh/megadlbot_oss/blob/master/mega/webserver/routes.py>
# Thanks to Eyaadh <https://github.com/eyaadh>

import re
import time
import math
import logging
import secrets
import mimetypes
from aiohttp import web
from aiohttp.http_exceptions import BadStatusLine
from WebStreamer.bot import multi_clients, work_loads
from WebStreamer.server.exceptions import FIleNotFound, InvalidHash
from WebStreamer import Var, utils, StartTime, __version__, StreamBot


routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(_):
    raise web.HTTPNotFound()
    # return web.json_response(
    #     {
    #         "server_status": "running",
    #         "uptime": utils.get_readable_time(time.time() - StartTime),
    #         "telegram_bot": "@" + StreamBot.username,
    #         "connected_bots": len(multi_clients),
    #         "loads": dict(
    #             ("bot" + str(c + 1), l)
    #             for c, (_, l) in enumerate(
    #                 sorted(work_loads.items(), key=lambda x: x[1], reverse=True)
    #             )
    #         ),
    #         "version": __version__,
    #     }
    # )


@routes.get("/{message_id}/{file_name}")
async def stream_handler(request: web.Request):
    try:
        message_id = int(request.match_info['message_id'])
        return await media_streamer(request, message_id)
    except ValueError as e:
        logging.error(e)
        raise web.HTTPNotFound()


@routes.get("/{type_channel}/{message_id}/{file_name}")
async def stream_handler(request):
    try:
        message_id = int(request.match_info['message_id'])
        type_channel = request.match_info['type_channel']
        #fname = request.match_info['file_name']
        if type_channel == "series":
            tchannel = -1001477968568
        if type_channel == "movie":
            tchannel = -1001449081541
        if type_channel == "subtitle":
            tchannel = -1001805531714
        if type_channel == "anime":
            tchannel = -1001227225876
        return await media_streamer(request, message_id, tchannel)
    except ValueError as e:
        logging.error(e)
        raise web.HTTPNotFound


class_cache = {}

async def media_streamer(request: web.Request, message_id: int, type_channel = None):
    range_header = request.headers.get("Range", 0)
    
    index = min(work_loads, key=work_loads.get)
    faster_client = multi_clients[index]
    
    if Var.MULTI_CLIENT:
        logging.info(f"Client {index} is now serving {request.remote}")

    if faster_client in class_cache:
        tg_connect = class_cache[faster_client]
        logging.debug(f"Using cached ByteStreamer object for client {index}")
    else:
        logging.debug(f"Creating new ByteStreamer object for client {index}")
        tg_connect = utils.ByteStreamer(faster_client)
        class_cache[faster_client] = tg_connect
    logging.debug("before calling get_file_properties")
    file_id = await tg_connect.get_file_properties(message_id, type_channel)
    logging.debug("after calling get_file_properties")
    
    file_size = file_id.file_size

    if range_header:
        from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = (request.http_range.stop or file_size) - 1
    
    if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes < from_bytes):
        return web.Response(
            status=416,
            body="416: Range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )
    
    chunk_size = 1024 * 1024
    until_bytes = min(until_bytes, file_size - 1)
    offset = from_bytes - (from_bytes % chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = until_bytes % chunk_size + 1

    req_length = until_bytes - from_bytes + 1
    part_count = math.ceil(until_bytes / chunk_size) - math.floor(offset / chunk_size)
    body = tg_connect.yield_file(
        file_id, index, offset, first_part_cut, last_part_cut, part_count, chunk_size
    )

    mime_type = file_id.mime_type
    file_name = utils.get_name(file_id)
    disposition = "attachment"

    
    if not mime_type:
        mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"

    if "video/" in mime_type or "audio/" in mime_type or "/html" in mime_type:
        disposition = "inline"

    return web.Response(
        status=206 if range_header else 200,
        body=body,
        headers={
            "Content-Type": f"{mime_type}",
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Length": str(req_length),
            "Content-Disposition": f'{disposition}; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        },
    )