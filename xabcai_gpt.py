import requests
from urllib.parse import quote
import json

def xabcai_gpt(model, user_prompt):
    user_prompt = json.dumps(user_prompt, ensure_ascii=False)
    prompt = quote(str(user_prompt))
    
    headers = {
        'authority': 'free.xabcai.com',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    
    data = "model=%s&prompts=%s" % (model, prompt) 
    
    response = requests.post('https://free.xabcai.com/chat', headers=headers, data=data, stream=True)
    return response

##example:
#import time
#model = "gpt-3.5-turbo-16k"
#user_ask = "列出五名唐朝诗人"
#args = '[{"role":"user","content":"%s"}]' % user_ask
#response = xabcai_gpt(model, args)
#for line in response.iter_lines():
#   if line:
#       output = line.decode('utf-8')
#       for char in output:
#           print(char, end='', flush=True)
#           time.sleep(0.05)
#       print("")