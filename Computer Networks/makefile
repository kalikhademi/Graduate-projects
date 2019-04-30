JFLAGS = -g
JC = javac
.SUFFIXES: .java .class
.java.class:
	$(JC) $(JFLAGS) $*.java

CLASSES = \
	Peer.java \
	PeerParser.java \
	CommonParser.java \
	FileManager.java \
	DataFile.java \
	SortByRate.java \
	Connection.java \
	Uploader.java \
	Client.java \
	peerProcess.java

default: classes

classes: $(CLASSES:.java=.class)

clean:
	$(RM) *.class
