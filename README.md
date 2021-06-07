# chunker
Chunk a file into multiple chunks and send the via a chosen medium

python3 chunker.py --file firmware.bin --chunk 32 --server test.mosquitto.org --port 1883 --topic ota/chunker