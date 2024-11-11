#!/usr/bin/env python

# creates manifest.json files in any folder that contains files in a hierarchy of folders
# based on:
# https://github.com/fair-research/bdbag/blob/master/doc/config.md#remote-file-manifest

# Example
# [
#     {
#         "url":"https://raw.githubusercontent.com/fair-research/bdbag/master/profiles/bdbag-profile.json",
#         "length":699,
#         "filename":"bdbag-profile.json",
#         "sha256":"eb42cbc9682e953a03fe83c5297093d95eec045e814517a4e891437b9b993139"
#     },
#     {
#         "url":"ark:/88120/r8059v",
#         "length": 632860,
#         "filename": "minid_v0.1_Nov_2015.pdf",
#         "sha256": "cacc1abf711425d3c554277a5989df269cefaa906d27f1aaa72205d30224ed5f"
#     }
# ]

import os
import sys
import json
import hashlib
import requests

# if len(sys.argv) != 2:
#     print(
#         """Usage: python 0_create_manifest.py <base_folder>
          
# base_folder should be the local path to the folder pointed by the
# FOLDER variable in the config.toml file."""
#     )
#     sys.exit(1)
# else:
#     base_folder = sys.argv[1]

baseurl = "https://web.corral.tacc.utexas.edu/setxuifl/"
BUFFER = 4 * 1073741824

for dirpath, dirnames, filenames in os.walk(base_folder):
    manifest = []
    for filename in filenames:
        if filename != "manifest.json":
            path = os.path.join(dirpath, filename)
            url = f"https://{baseurl}/{path}"
            
            # Get file via HTTP request
            response = requests.get(url, stream=True)
            sha512 = hashlib.sha512()
            length = 0
            
            for chunk in response.iter_content(chunk_size=BUFFER):
                if chunk:
                    length += len(chunk)
                    sha512.update(chunk)
            
            manifest.append({
                "sha512": sha512.hexdigest(),
                "filename": os.path.join(
                    endpoint["FOLDER"],
                    dirpath.replace(base_folder + "/", ""),
                    filename,
                ),
                "url": url,
                "length": length,
            })

    if len(filenames) > 0:
        with open(os.path.join(dirpath, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=4)
        print(dirpath)
