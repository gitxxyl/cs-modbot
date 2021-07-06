import time
# TODO: implement vt scan in on_message with attachments
import vt
def scan():
    global analysis
    # TODO: Store virustotal API Keys in env
    vt_key = "aafa3531e088d440658570a3059046ac7b4bb304f25f4293e25440959e0d522c" #
    fp = ""  # filepath to test virustotal (emptied for commit)
    vt_client = vt.Client(vt_key)  # init virustotal client
    with open(fp, "rb") as f:
        analysis = vt_client.scan_file(f, wait_for_completion=True)
    s = analysis.status  # scan results

    if s['suspicious'] == s['malicious'] == s['harmless'] == 0:  # file is OK
        return True
    else:
        # TODO: handle sus file
        return False

