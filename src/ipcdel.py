import wgdb
for i in ["1001", "1002", "1003"]:
	try:
		wgdb.delete_database(i)
	except:
		pass
