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
    fp.seek(0)
    return hash.hexdigest()


async def handlePositive(file, response, msg) -> None:
    """Perform necessary tasks to deal with a virus-positive attachment."""
    await debug.log(f"Suspicious file detected! \n\tAuthor: {msg.author}  \n\tSHA-256: {gethash(file.fp)}\n\t{response['data']['attributes']['stats']['suspicious']} suspicious and {response['data']['attributes']['stats']['malicious']} malicious responses.")
    await msg.delete()


async def scanf(file: discord.File, msg: discord.Message) -> bool:
    """Check if file is a virus."""
    urlf = "https://www.virustotal.com/api/v3/files"
    urla = "https://www.virustotal.com/api/v3/analyses"
    headers = {'x-apikey': 'aafa3531e088d440658570a3059046ac7b4bb304f25f4293e25440959e0d522c'}
    files = {'file': (file.filename, file.fp)}
    hash = str(gethash(file.fp))
    response = requests.get(url=urlf + f"/{hash}/analyse", headers=headers)
    while response.status_code != 200:
        id = requests.post(url=urlf, headers=headers, files=files).json()["data"]["id"]
        await asyncio.sleep(10)
        response = requests.get(url=urla + f"/{id}", headers=headers)
    response = response.json()
    if response['data']['attributes']['stats']['suspicious'] == response['data']['attributes']['stats']['malicious'] == 0:
        await msg.clear_reaction("⌛")
        await msg.add_reaction("✅")
        return False
    else:
        await handlePositive(file, response, msg)
        return True

