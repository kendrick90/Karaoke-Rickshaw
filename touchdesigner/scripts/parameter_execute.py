import TDJSON
import json
import TDFunctions

container = parent().par.Container

operator = op(container)

def getContainerUpdate(names):
	
	# schema = TDJSON.opToJSONOp(operator, extraAttrs=None, forceAttrLists=True, includeCustomPages=True, includeBuiltInPages=parent().par.Includebuiltinsettings)
	info = TDFunctions.getParInfo(operator, pattern='*', names=None, includeCustom=True, includeNonCustom=False)
	openFolder = bool(parent().par.Openui)
	useMinMax = bool(parent().par.Useminmax)
	uiParams = {'openFolder': openFolder, 'useMinMax': useMinMax}
	stateChanges = {}
	if names and len(names) > 0:
		for name in names:
			stateChanges[name] = info[name]
	return {'uiParams': uiParams, 'componentName': str(container), 'info' : stateChanges}

async def sendAsnycData(params):
	data = getContainerUpdate(params)
	op('websocket1').sendText(json.dumps(data))

def sendData(params=None):
	coroutines = [sendAsnycData(params)]
	op.TDAsyncIO.Run(coroutines)
	

	

def onValueChange(par, prev):
	print(par.name, par.eval())
	#if par.eval() == prev:
	#	return
	sendData([par.name])
	# use par.eval() to get current value
	return

# Called at end of frame with complete list of individual parameter changes.
# The changes are a list of named tuples, where each tuple is (Par, previous value)
def onValuesChanged(changes):
	
	names = []
	for c in changes:
		if c.par.eval() == c.prev:
			continue
		names.append(c.par.name)
	sendData(names)
	return

def onPulse(par):
	sendData([par.name])
	return

def onExpressionChange(par, val, prev):
	sendData([par.name])
	return

def onExportChange(par, val, prev):
	sendData()
	return

def onEnableChange(par, val, prev):
	sendData([par.name])
	return

def onModeChange(par, val, prev):
	sendData([par.name])
	return
	