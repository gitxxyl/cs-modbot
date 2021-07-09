"""
**virusscanner.py**\n
Virus scanner file to scan for viruses on incoming discord messages. \n
|
"""
import typing

import discord
import requests
import hashlib
from dotenv import dotenv_values

import config
import debug


def gethash(fp: typing.IO) -> str:
    """
    Hashes object to be uploaded to the VirusTotal API.

    :param fp: File-like object to be hashed. Can be any readable object.
    :type fp: typing.IO
    :return: Returns hash of object as a hex string.
    :rtype: str \n
    |
    """
    chunksize = 65536  # process file in 64kb chunks to reduce memory usage spikes
    hsh = (getattr(hashlib, config.hashtype))()  # use hashtype specified in config file
    currentchunk = 0
    while currentchunk != b'':
        currentchunk = fp.read(chunksize)
        hsh.update(currentchunk)
    fp.seek(0)
    return hsh.hexdigest()  # converts hash to hex string


async def handlePositive(file: discord.File, response: dict, msg: discord.Message) -> None:
    """
    Perform necessary tasks to deal with a virus-positive attachment.

    :param file: File to be processed.
    :type file: discord.File
    :param msg: Original message with file attachment.
    :type msg: discord.Message
    :param response: VirusTotal API response. JSON.
    :type response: dict

    :return: None
    :rtype: None \n
    |
    """
    await debug.log(  # Logs malicious file detection
        f"Suspicious file detected! \n\tAuthor: {msg.author}  \n\tSHA-256: {gethash(file.fp)}\n\t{response['data']['attributes']['stats']['suspicious']} suspicious and {response['data']['attributes']['stats']['malicious']} malicious responses.")
    await msg.delete()


async def scanf(file: discord.File, msg: discord.Message) -> bool:
    """
    Scans a file with the VirusTotal v3 Api.

    :param file: File to be processed. Instance of discord.File.
    :type file: discord.File
    :param msg: Original message with file attachment. Instance of discord.Message.
    :type msg: discord.Message

    :return: Returns True if virus found, False if not found.
    :rtype: bool \n
    |
    """

    # REST arguments
    urlf = "https://www.virustotal.com/api/v3/files"  # File upload endpoint
    urla = "https://www.virustotal.com/api/v3/analyses"  # File analysis endpoint
    headers = {'x-apikey': dotenv_values(".env")['VT_TOKEN']}  # Adds gitxxyl's VirusTotal API key to header of all requests.
    files = {'file': (file.filename, file.fp)}
    hsh = gethash(file.fp)  # SHA-256 hash of file to be uploaded

    response = requests.get(url=urlf + f"/{hsh}/analyse",
                            headers=headers)  # try fetching existing file analysis from vt (mostly fails)

    # Upload file and get virus analysis
    while response.status_code != 200:  # run until no HTTPS errors
        analysis_id = requests.post(url=urlf, headers=headers, files=files).json()["data"]["id"]
        # await asyncio.sleep(10)  # was neeeded to limit public API calls, now obsolete
        response = requests.get(url=urla + f"/{analysis_id}", headers=headers)

    response = response.json()  # convert HTTPS response to json to process
    stats = response['data']['attributes']['stats']  # get virus analysis stats

    if stats['suspicious'] == stats['malicious'] == 0:  # file is clear, no malware
        await msg.clear_reaction("⌛")
        await msg.add_reaction("✅")
        return False
    else:  # malware detected by at least one AV provider
        await handlePositive(file, response, msg)
        return True
