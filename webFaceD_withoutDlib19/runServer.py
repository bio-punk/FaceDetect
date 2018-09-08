# -*- coding: utf-8 -*-

from os import environ
from webFaceD import app

app.logger.info(u"""
                ___.   ___________                       ________    
__  _  __  ____ \_ |__ \_   _____/_____     ____   ____  \______ \   
\ \/ \/ /_/ __ \ | __ \ |    __)  \__  \  _/ ___\_/ __ \  |    |  \  
 \     / \  ___/ | \_\ \|     \    / __ \_\  \___\  ___/  |    `   \ 
  \/\_/   \___  >|___  /\___  /   (____  / \___  >\___  >/_______  / 
              \/     \/     \/         \/      \/     \/         \/  

	""")

print (u"""

                ___.   ___________                       ________    
__  _  __  ____ \_ |__ \_   _____/_____     ____   ____  \______ \   
\ \/ \/ /_/ __ \ | __ \ |    __)  \__  \  _/ ___\_/ __ \  |    |  \  
 \     / \  ___/ | \_\ \|     \    / __ \_\  \___\  ___/  |    `   \ 
  \/\_/   \___  >|___  /\___  /   (____  / \___  >\___  >/_______  / 
              \/     \/     \/         \/      \/     \/         \/  

	""")

if __name__ == '__main__':
	HOST = environ.get('SERVER_HOST', 'localhost')
	try:
		PORT = int(environ.get('SERVER_PORT', '5555'))
	except ValueError:
		PORT = 5555

	#多线程模式
	#app.run(HOST, PORT, threaded=True)

	#多进程模式
	#app.run(HOST, PORT, processes=3)

	app.run(HOST, PORT, debug=True)
