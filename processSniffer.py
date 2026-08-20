import psutil


activeProcesses = set()
def processSniffer():
    
    for process in psutil.process_iter(['pid', 'name']):
        print(process.info)
        activeProcesses.add(process.info['name'].lower())
processSniffer()#test
print(activeProcesses)

