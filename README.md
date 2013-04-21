tvonline
========

TVOnline consists of a backend and a frontend application that allows different
video and audio streams to be consumed over the internet through the browser or
external video players.

Front-End:

An Python-Tornado web app that keeps track of the status of registered stream 
servers and streams hosted on them. General users can choose to watch any of the
running streams. Administrators can further remotely turn on/off stream servers
and reconfigure streams.

Back-End:

The python back-end is currently only running on Linux servers that have VLC
installed. It is a simple secure XML-RPC service that start/stops streams upon
requests from Administrators. Moreover, each server also manages its upload and
further accepts shutdown requests from Administrators. Currently there is only
support for dvb-s tv streams, but DVD, file, or other stream types could easily
be added.
