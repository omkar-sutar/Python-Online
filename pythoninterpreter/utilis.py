import docker
import os
import random
import string
import time

def fill_precode(id,file):
    code=f'''
import sys
sys.stdout=open("output_{id}.txt",'w')
sys.stdin=open("input_{id}.txt",'r')
sys.stderr=sys.stdout
'''
    file.write(code)

#run code and return its output as string
def execute_code(code,input)->str:
    client=docker.from_env()
    #container, files will have this id at suffix
    id=''.join(random.choices(string.ascii_lowercase, k=5))
    container_name='container_'+id
    container=client.containers.run("pythonlightimg",remove=True,detach=True,name=container_name,mem_limit="512m",stdin_open=True)
    if 'tmp' not in os.listdir():
        os.mkdir('tmp')
    file=open(f"tmp/input_{id}.txt",'w')
    file.write(input)
    file.close()
    file=open(f"tmp/main_{id}.py",'w')
    fill_precode(id,file)
    file.write(code)
    file.close()
    os.system(f'docker cp tmp/input_{id}.txt {container_name}:app/')
    os.system(f'docker cp tmp/main_{id}.py {container_name}:app/')
    container.exec_run(cmd=f"python3 main_{id}.py")
    os.system(f'docker cp {container_name}:app/output_{id}.txt tmp/')
    container.kill()
    #if some dumbass deletes output.txt from his 'app/' it wont get copied
    #so make sure it exists; if it doesnt exists it will be created (open in append mode)
    file=open(f"tmp/output_{id}.txt",'a+')
    file.close()
    file=open(f"tmp/output_{id}.txt",'r')
    output=file.read()
    file.close()
    os.remove(f"tmp/output_{id}.txt")
    os.remove(f"tmp/input_{id}.txt")
    os.remove(f"tmp/main_{id}.py")
    return output

