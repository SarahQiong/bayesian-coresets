import numpy as np
import bokeh.plotting as bkp
import bokeh.io as bki
import bokeh.layouts as bkl
from bokeh.models import FuncTickFormatter
import bokeh.models as bkm
import bokeh.palettes 
import time

logFmtr = FuncTickFormatter(code="""
var trns = [
'\u2070',
'\u00B9',
'\u00B2',
'\u00B3',
'\u2074',
'\u2075',
'\u2076',
'\u2077',
'\u2078',
'\u2079'];
var tick_power = Math.floor(Math.log10(tick));
var tick_mult = Math.pow(10, Math.log10(tick) - tick_power);
var ret = '';
if (tick_mult > 1.) {
  if (Math.abs(tick_mult - Math.round(tick_mult)) > 0.05){
    ret = tick_mult.toFixed(1) + '\u22C5';
  } else {
    ret = tick_mult.toFixed(0) +'\u22C5';
  }
}
ret += '10';
if (tick_power < 0){
  ret += '\u207B';
  tick_power = -tick_power;
}
power_digits = []
while (tick_power > 9){
  power_digits.push( tick_power - Math.floor(tick_power/10)*10 )
  tick_power = Math.floor(tick_power/10)
}
power_digits.push(tick_power)
for (i = power_digits.length-1; i >= 0; i--){
  ret += trns[power_digits[i]];
}
return ret;
""")



dnames = ['poiss/synth', 'poiss/biketrips', 'poiss/airportdelays', 'lr/synth', 'lr/ds1', 'lr/phishing']

fig_cput = bkp.figure(y_axis_type='log', y_axis_label='Normalized Fisher Information Distance', x_axis_type='log', x_axis_label='Relative Total CPU Time', x_range=(.05, 1.1), plot_width=1250, plot_height=1250)
fig_csz = bkp.figure(y_axis_type='log', y_axis_label='Normalized Fisher Information Distance', x_axis_type='log', x_axis_label='Coreset Size', plot_width=1250, plot_height=1250)

axis_font_size='36pt'
legend_font_size='36pt'
for f in [fig_cput, fig_csz]:
  f.xaxis.axis_label_text_font_size= axis_font_size
  f.xaxis.major_label_text_font_size= axis_font_size
  f.yaxis.axis_label_text_font_size= axis_font_size
  f.yaxis.major_label_text_font_size= axis_font_size
  f.yaxis.formatter = logFmtr
fig_cput.xaxis.ticker = bkm.tickers.FixedTicker(ticks=[.1, .5, 1])
fig_csz.xaxis.formatter = logFmtr


pal = bokeh.palettes.colorblind['Colorblind'][8]
pal = [pal[0], pal[1], '#d62728', pal[3], pal[4], pal[5], pal[6], pal[7], pal[2]]
for didx, dnm in enumerate(dnames):
  
  res = np.load(dnm  + '_results.npz')

  Fs = res['Fs']
  cputs = res['cputs']
  cputs_full = res['cputs_full']
  csizes = res['csizes']
  anms = res['anms']

  for aidx, anm in enumerate(anms):
    if anm == 'FW':
      clr = pal[1]
    elif anm == 'GIGA':
      clr = pal[0]
    else:
      clr = pal[2]

    fig_cput.line(np.percentile(cputs[aidx,:,:], 50, axis=0)/np.percentile(cputs_full, 50, axis=0), np.percentile(Fs[aidx, :, :], 50, axis=0)/np.percentile(Fs[2, :, :], 50), line_color=clr, line_width=8, legend=anm)
    fig_csz.line(np.percentile(csizes[aidx,:,:], 50, axis=0), np.percentile(Fs[aidx, :, :], 50, axis=0)/np.percentile(Fs[2, :, :], 50), line_color=clr, line_width=8, legend=anm)
    
rndlbl = bkm.Label(x=1.0, x_offset=-10, y=700, y_units='screen', text='Full Dataset MCMC', angle=90, angle_units='deg', text_font_size='30pt')
rndspan = bkm.Span(location = 1.0, dimension='height', line_width=8, line_color='black', line_dash='40 40')
fig_cput.add_layout(rndspan)
fig_cput.add_layout(rndlbl)

for f in [fig_cput, fig_csz]:
  f.legend.label_text_font_size= legend_font_size
  f.legend.glyph_width=40
  f.legend.glyph_height=80
  f.legend.spacing=20
  f.legend.orientation='horizontal'

bkp.show(bkl.gridplot([[fig_cput, fig_csz]]))
#bkp.save(bkl.gridplot([[fig_cput, fig_csz]]))

