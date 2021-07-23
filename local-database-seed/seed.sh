mongoimport --host mongo --db ethtx --collection contracts --type json --mode upsert --file /contracts.json
mongoimport --host mongo --db ethtx --collection addresses --type json --mode upsert --file /addresses.json
