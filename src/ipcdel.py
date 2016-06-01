import wgdb
for i in ["configuration_cache", "metrics_cache", "discovery_cache"]:
	try:
		wgdb.delete_database(i)
	except:
		pass
