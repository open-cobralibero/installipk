from os import unlink
from twisted.internet import reactor
try:
	from urllib.request import urlopen, Request
except ImportError:
	from urllib2 import urlopen, Request, HTTPError, URLError

from enigma import eTimer

class DownloadWithProgress:
	def __init__(self, url, outputFile):
		self.url = url
		self.outputFile = outputFile
		self.userAgent = "Enigma2 HbbTV/1.1.1 (+PVR+RTSP+DL;GIOPPYGIO;;;)"
		self.totalSize = 0
		self.progress = 0
		self.progressCallback = None
		self.endCallback = None
		self.errorCallback = None
		self.stopFlag = False
		self.timer = eTimer()
		self.timer.callback.append(self.reportProgress)

	def start(self):
		try:
			request = Request(self.url, None, {"User-agent": self.userAgent})
			feedFile = urlopen(request)
			metaData = feedFile.headers
			self.totalSize = int(metaData.get("Content-Length", 0))
			# Set the transfer block size to a minimum of 1K and a maximum of 1% of the file size (or 128KB if the size is unknown) else use 64K.
			self.blockSize = max(min(self.totalSize // 100, 1024), 131071) if self.totalSize else 65536
		except OSError as err:
			if self.errorCallback:
				self.errorCallback(err)
			return self
		reactor.callInThread(self.run)
		return self

	def run(self):
		import requests
		response = requests.get(self.url, headers={"User-agent": self.userAgent}, stream=True)
		try:
			with open(self.outputFile, "wb") as fd:
				for buffer in response.iter_content(self.blockSize):
					if self.stopFlag:
						response.close()
						fd.close()
						unlink(self.outputFile)
						return True
					self.progress += len(buffer)
					if self.progressCallback:
						self.timer.start(0, True)
					fd.write(buffer)
			if self.endCallback:
				self.endCallback(self.outputFile)
		except OSError as err:
			self.errorCallback(err)
		return False

	def stop(self):
		self.stopFlag = True

	def reportProgress(self):
		self.progressCallback(self.progress, self.totalSize)

	def addProgress(self, progressCallback):
		self.progressCallback = progressCallback

	def addEnd(self, endCallback):
		self.endCallback = endCallback

	def addError(self, errorCallback):
		self.errorCallback = errorCallback

	def setAgent(self, userAgent):
		self.userAgent = userAgent

	def addErrback(self, errorCallback):
		self.errorCallback = errorCallback
		return self

	def addCallback(self, endCallback):
		self.endCallback = endCallback
		return self


class downloadWithProgress(DownloadWithProgress):
	pass
