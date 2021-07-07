"""Virus scanner file to scan for viruses on incoming discord messages."""
import asyncio

import discord
import requests
import enum
import hashlib
from dotenv import dotenv_values

import config
import debug


def gethash(fp) -> str:
    chunksize = 65536  # process file in 64kb chunks to reduce memory usage spikes
    hash = (getattr(hashlib, config.hashtype))()
    currentchunk = 0
    while currentchunk != b'':
        currentchunk = fp.read(chunksize)
        hash.update(currentchunk)

    return hash.hexdigest()


async def handlePositive(file, response, msg) -> None:
    """Perform necessary tasks to deal with a virus-positive attachment."""
    await debug.log(f"Suspicious file detected! \nAuthor: {msg.author}  \nSHA-256: {gethash(file.fp)}")
    await msg.delete()

async def scanf(file: discord.File = None, msg: discord.Message = None) -> bool:
    """Check if"""
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': dotenv_values(".env")["VT_TOKEN"], 'resource': gethash(file.fp)}
    response = requests.get(url, params=params).json()
    if response["response_code"] != 1:
        response = await newscanf(file)
    if response["positives"] >= 1:
        await handlePositive(file=file, response=response, msg=msg)
        return False
    else:
        return True


async def newscanf(file: discord.File = None) -> dict:
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    files = {'file': (file.filename, file.fp)}
    params = {'apikey': dotenv_values(".env")["VT_TOKEN"]}
    response = requests.post(url, files=files, params=params).json()
    while response["response_code"] == -2:
        response = requests.post(url, files=files, params=params).json()
        await asyncio.sleep(2)

    return response


