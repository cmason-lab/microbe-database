import microbe_directory.python_api

md = microbe_directory.python_api.MicrobeDirectory('data/microbe_directory.sql')


print(md.get_optimal_temperature_column())
#print(md.get_microbe('Acidilobus saccharovorans')['phylum'])