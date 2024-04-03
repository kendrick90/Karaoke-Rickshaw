# me - this DAT
# dat - the WebSocket DAT
import TDJSON
import json
import TDFunctions

container = parent().par.Container # Touchdesigner container to get parameters from

operator = op(container)

def getContainerDetail():
	container = parent().par.Container
	operator = op(container)
	includeBuiltIn = parent().par.Includebuiltinsettings
	schema = TDJSON.opToJSONOp(operator, extraAttrs=None, forceAttrLists=True, includeCustomPages=True, includeBuiltInPages=includeBuiltIn)
	info = TDFunctions.getParInfo(operator, pattern='*', names=None, includeCustom=True, includeNonCustom=includeBuiltIn)
	openFolder = bool(parent().par.Openui)
	useMinMax = bool(parent().par.Useminmax)
	uiParams = {'openFolder': openFolder, 'useMinMax': useMinMax}
	return {'uiParams' : uiParams, 'componentName': str(container), 'schema' : schema, 'info' : info}

def onConnect(dat):
	#data = getContainerDetail()
	
	#msg = json.dumps(data)
	#op('text1').text = msg
	#dat.sendText(msg)

	#print(parent().name + ' connected')
	return

# me - this DAT
# dat - the WebSocket DAT

def onDisconnect(dat):
	return
	
async def parseJSON(message, dat):
	data = json.loads(message)
	if 'getComponentData' in data:
		data = getContainerDetail()
		dat.sendText(json.dumps(data))
	elif 'GUIUpdate' in data:
		componentName = data['componentName']
		if componentName == container:
			info = data['info']
			TDFunctions.applyParInfo(op(componentName), info, setDefaults=False)
			if 'pulse' in data and len(data['pulse']) > 0:
				for opName in data['pulse']:
					op(componentName).par[opName].pulse()
			

def onReceiveText(dat, rowIndex, message):
	if message == 'ping':
		dat.sendText('pong')
		return
	
	coroutines = [parseJSON(message, dat)]
	op.TDAsyncIO.Run(coroutines)
	# data = json.loads(message)
	# if 'getComponentData' in data:
	# 	data = getContainerDetail()
	# 	dat.sendText(json.dumps(data))
	# elif 'GUIUpdate' in data:
	# 	componentName = data['componentName']
	# 	if componentName == container:
	# 		info = data['info']
	# 		TDFunctions.applyParInfo(op(componentName), info, setDefaults=False)
		
	return

# me - this DAT
# dat - the DAT that received a message
# contents - a byte array of the message contents
# 
# Only binary frame messages will be handled in this function.

def onReceiveBinary(dat, contents):
	return

# me - this DAT
# dat - the DAT that received a message
# contents - a byte array of the message contents
# 
# Only ping messages will be handled in this function.

def onReceivePing(dat, contents):
	dat.sendPong(contents) # send a reply with same message
	return

# me - this DAT
# dat - the DAT that received a message
# contents - a byte array of the message content
# 
# Only pong messages will be handled in this function.

def onReceivePong(dat, contents):
	return


# me - this DAT
# dat - the DAT that received a message
# message - a unicode representation of the message
#
# Use this method to monitor the websocket status messages

def onMonitorMessage(dat, message):
	return

	