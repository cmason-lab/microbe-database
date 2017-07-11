import microbe_directory.python_api
import microbe_directory.plotter

md = microbe_directory.python_api.MicrobeDirectory('data/microbe_directory_7-10-17.sql')
plt = microbe_directory.plotter.Plotter()

temps = md.get_optimal_temperature_column()
phs = md.get_optimal_ph_column()

plt.plot_column(temps, 'Optimal Temperature (°C)')
plt.plot_column(phs, 'Optimal pH')